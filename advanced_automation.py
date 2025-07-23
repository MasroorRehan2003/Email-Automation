"""
Advanced Email Automation System with Scheduling and Batch Processing
This script extends the basic email automation with advanced features
"""

import schedule
import time
import os
import glob
from datetime import datetime, timedelta
from email_automation import EmailAutomation
from config import EMAIL_CONFIG, EMAIL_TEMPLATES
import json

class AdvancedEmailAutomation(EmailAutomation):
    def __init__(self):
        super().__init__(
            EMAIL_CONFIG['EMAIL_USER'], 
            EMAIL_CONFIG['EMAIL_PASS'],
            EMAIL_CONFIG['SMTP_SERVER'],
            EMAIL_CONFIG['SMTP_PORT']
        )
        self.sent_files_log = 'sent_files.json'
        self.load_sent_files_log()
    
    def load_sent_files_log(self):
        """Load the log of previously sent files"""
        try:
            with open(self.sent_files_log, 'r') as f:
                self.sent_files = json.load(f)
        except FileNotFoundError:
            self.sent_files = {}
    
    def save_sent_files_log(self):
        """Save the log of sent files"""
        with open(self.sent_files_log, 'w') as f:
            json.dump(self.sent_files, f, indent=2)
    
    def mark_file_as_sent(self, file_path, recipient):
        """Mark a file as sent to prevent duplicate sends"""
        file_key = f"{file_path}:{recipient}"
        self.sent_files[file_key] = datetime.now().isoformat()
        self.save_sent_files_log()
    
    def is_file_already_sent(self, file_path, recipient, hours_threshold=24):
        """Check if file was already sent to recipient within threshold"""
        file_key = f"{file_path}:{recipient}"
        if file_key in self.sent_files:
            sent_time = datetime.fromisoformat(self.sent_files[file_key])
            time_diff = datetime.now() - sent_time
            return time_diff.total_seconds() < (hours_threshold * 3600)
        return False
    
    def send_new_files_from_folder(self, folder_path, recipients, template='DATA_REPORT', file_pattern='*'):
        """
        Send only new files from a folder to recipients
        """
        pattern = os.path.join(folder_path, file_pattern)
        files = glob.glob(pattern)
        
        sent_count = 0
        skipped_count = 0
        
        for file_path in files:
            if os.path.isfile(file_path):
                for recipient in recipients:
                    if not self.is_file_already_sent(file_path, recipient):
                        # Get template
                        template_data = EMAIL_TEMPLATES.get(template, EMAIL_TEMPLATES['CUSTOM'])
                        filename = os.path.basename(file_path)
                        
                        subject = template_data['subject'].format(filename=filename)
                        body = template_data['body'].format(filename=filename)
                        
                        success = self.send_email_with_attachment(
                            to_email=recipient,
                            subject=subject,
                            body=body,
                            attachment_path=file_path
                        )
                        
                        if success:
                            self.mark_file_as_sent(file_path, recipient)
                            sent_count += 1
                        else:
                            print(f"Failed to send {filename} to {recipient}")
                    else:
                        skipped_count += 1
                        print(f"Skipped {os.path.basename(file_path)} for {recipient} (already sent)")
        
        print(f"Batch complete: {sent_count} emails sent, {skipped_count} skipped")
        return sent_count, skipped_count
    
    def schedule_daily_reports(self, folder_path, recipients, time_str="09:00"):
        """Schedule daily email reports"""
        def daily_job():
            print(f"Running daily report job at {datetime.now()}")
            self.send_new_files_from_folder(folder_path, recipients, 'DATA_REPORT')
        
        schedule.every().day.at(time_str).do(daily_job)
        print(f"Scheduled daily reports at {time_str}")
    
    def schedule_weekly_reports(self, folder_path, recipients, day="monday", time_str="09:00"):
        """Schedule weekly email reports"""
        def weekly_job():
            print(f"Running weekly report job at {datetime.now()}")
            self.send_new_files_from_folder(folder_path, recipients, 'WEEKLY_UPDATE')
        
        getattr(schedule.every(), day.lower()).at(time_str).do(weekly_job)
        print(f"Scheduled weekly reports on {day} at {time_str}")
    
    def monitor_folder_for_new_files(self, folder_path, recipients, check_interval=300):
        """
        Monitor folder for new files and send them automatically
        check_interval: seconds between checks (default 5 minutes)
        """
        print(f"Monitoring folder: {folder_path}")
        print(f"Check interval: {check_interval} seconds")
        
        known_files = set(glob.glob(os.path.join(folder_path, '*')))
        
        while True:
            current_files = set(glob.glob(os.path.join(folder_path, '*')))
            new_files = current_files - known_files
            
            if new_files:
                print(f"Found {len(new_files)} new files")
                for file_path in new_files:
                    if os.path.isfile(file_path):
                        for recipient in recipients:
                            filename = os.path.basename(file_path)
                            subject = f"New File Alert - {filename}"
                            body = f"A new file has been detected: {filename}\n\nAutomatic analysis below:"
                            
                            self.send_email_with_attachment(
                                to_email=recipient,
                                subject=subject,
                                body=body,
                                attachment_path=file_path
                            )
                            self.mark_file_as_sent(file_path, recipient)
                
                known_files = current_files
            
            time.sleep(check_interval)

def main():
    """Main function with menu-driven interface"""
    automation = AdvancedEmailAutomation()
    
    print("Advanced Email Automation System")
    print("=" * 50)
    print("1. Send new files from folder (one-time)")
    print("2. Schedule daily reports")
    print("3. Schedule weekly reports") 
    print("4. Monitor folder for new files (continuous)")
    print("5. View sent files log")
    print("6. Clear sent files log")
    print("7. Run scheduled jobs (blocking)")
    
    choice = input("\nEnter your choice (1-7): ")
    
    if choice == "1":
        folder = input("Enter folder path: ")
        recipients = input("Enter recipient emails (comma-separated): ").split(',')
        recipients = [email.strip() for email in recipients]
        
        sent, skipped = automation.send_new_files_from_folder(folder, recipients)
        print(f"Completed: {sent} sent, {skipped} skipped")
    
    elif choice == "2":
        folder = input("Enter folder path: ")
        recipients = input("Enter recipient emails (comma-separated): ").split(',')
        recipients = [email.strip() for email in recipients]
        time_str = input("Enter time (HH:MM, default 09:00): ") or "09:00"
        
        automation.schedule_daily_reports(folder, recipients, time_str)
        print("Daily reports scheduled. Run option 7 to start the scheduler.")
    
    elif choice == "3":
        folder = input("Enter folder path: ")
        recipients = input("Enter recipient emails (comma-separated): ").split(',')
        recipients = [email.strip() for email in recipients]
        day = input("Enter day (monday-sunday, default monday): ") or "monday"
        time_str = input("Enter time (HH:MM, default 09:00): ") or "09:00"
        
        automation.schedule_weekly_reports(folder, recipients, day, time_str)
        print("Weekly reports scheduled. Run option 7 to start the scheduler.")
    
    elif choice == "4":
        folder = input("Enter folder path: ")
        recipients = input("Enter recipient emails (comma-separated): ").split(',')
        recipients = [email.strip() for email in recipients]
        interval = int(input("Enter check interval in seconds (default 300): ") or "300")
        
        print("Starting folder monitoring... Press Ctrl+C to stop")
        try:
            automation.monitor_folder_for_new_files(folder, recipients, interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    
    elif choice == "5":
        print("\nSent Files Log:")
        print("-" * 30)
        for file_recipient, timestamp in automation.sent_files.items():
            print(f"{timestamp}: {file_recipient}")
    
    elif choice == "6":
        automation.sent_files = {}
        automation.save_sent_files_log()
        print("Sent files log cleared.")
    
    elif choice == "7":
        print("Starting scheduled job runner... Press Ctrl+C to stop")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
