import smtplib
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import json
import csv
from pathlib import Path
import logging
from datetime import datetime

# Email configuration
EMAIL_USER = 'i211707@nu.edu.pk'
EMAIL_PASS = 'uaosbqwpuemmioob'  # Gmail App Password
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_automation.log'),
        logging.StreamHandler()
    ]
)

class EmailAutomation:
    def __init__(self, email_user, email_pass, smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT):
        self.email_user = email_user
        self.email_pass = email_pass
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def analyze_file_content(self, file_path):
        """
        Analyze file content and return a description based on file type
        """
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        file_size = os.path.getsize(file_path)
        
        description = f"File: {file_path.name}\n"
        description += f"Size: {self._format_file_size(file_size)}\n"
        description += f"Type: {file_extension or 'No extension'}\n\n"
        
        try:
            if file_extension in ['.csv']:
                description += self._analyze_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                description += self._analyze_excel(file_path)
            elif file_extension in ['.json']:
                description += self._analyze_json(file_path)
            elif file_extension in ['.txt', '.log']:
                description += self._analyze_text(file_path)
            elif file_extension in ['.pdf']:
                description += "PDF document - Contains formatted text and possibly images"
            elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                description += "Image file - Visual content"
            elif file_extension in ['.doc', '.docx']:
                description += "Word document - Text document with formatting"
            elif file_extension in ['.py']:
                description += self._analyze_python(file_path)
            else:
                description += f"File type: {file_extension} - Binary or specialized format"
                
        except Exception as e:
            description += f"Could not analyze file content: {str(e)}"
            
        return description
    
    def _format_file_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def _analyze_csv(self, file_path):
        """Analyze CSV file content"""
        try:
            df = pd.read_csv(file_path)
            description = f"CSV Data Analysis:\n"
            description += f"- Rows: {len(df)}\n"
            description += f"- Columns: {len(df.columns)}\n"
            description += f"- Column names: {', '.join(df.columns.tolist()[:10])}"
            if len(df.columns) > 10:
                description += f" ... and {len(df.columns) - 10} more"
            description += "\n"
            
            # Sample data types
            description += f"- Data types: {dict(df.dtypes.value_counts())}\n"
            return description
        except Exception as e:
            return f"CSV file - Could not analyze: {str(e)}\n"
    
    def _analyze_excel(self, file_path):
        """Analyze Excel file content"""
        try:
            df = pd.read_excel(file_path)
            description = f"Excel Data Analysis:\n"
            description += f"- Rows: {len(df)}\n"
            description += f"- Columns: {len(df.columns)}\n"
            description += f"- Column names: {', '.join(df.columns.tolist()[:10])}"
            if len(df.columns) > 10:
                description += f" ... and {len(df.columns) - 10} more"
            description += "\n"
            return description
        except Exception as e:
            return f"Excel file - Could not analyze: {str(e)}\n"
    
    def _analyze_json(self, file_path):
        """Analyze JSON file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            description = f"JSON Data Analysis:\n"
            if isinstance(data, dict):
                description += f"- Type: Dictionary/Object\n"
                description += f"- Keys: {list(data.keys())[:10]}\n"
            elif isinstance(data, list):
                description += f"- Type: Array/List\n"
                description += f"- Items: {len(data)}\n"
                if data and isinstance(data[0], dict):
                    description += f"- First item keys: {list(data[0].keys())[:5]}\n"
            else:
                description += f"- Type: {type(data).__name__}\n"
            
            return description
        except Exception as e:
            return f"JSON file - Could not analyze: {str(e)}\n"
    
    def _analyze_text(self, file_path):
        """Analyze text file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            words = content.split()
            
            description = f"Text File Analysis:\n"
            description += f"- Lines: {len(lines)}\n"
            description += f"- Words: {len(words)}\n"
            description += f"- Characters: {len(content)}\n"
            
            # Show first few lines as preview
            if lines:
                description += f"- Preview (first 3 lines):\n"
                for i, line in enumerate(lines[:3]):
                    description += f"  {i+1}: {line[:50]}{'...' if len(line) > 50 else ''}\n"
            
            return description
        except Exception as e:
            return f"Text file - Could not analyze: {str(e)}\n"
    
    def _analyze_python(self, file_path):
        """Analyze Python file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            imports = [line.strip() for line in lines if line.strip().startswith(('import ', 'from '))]
            functions = [line.strip() for line in lines if line.strip().startswith('def ')]
            classes = [line.strip() for line in lines if line.strip().startswith('class ')]
            
            description = f"Python File Analysis:\n"
            description += f"- Lines of code: {len(lines)}\n"
            description += f"- Imports: {len(imports)}\n"
            description += f"- Functions: {len(functions)}\n"
            description += f"- Classes: {len(classes)}\n"
            
            if imports:
                description += f"- Key imports: {', '.join(imports[:5])}\n"
            if functions:
                description += f"- Functions: {', '.join([f.split('(')[0].replace('def ', '') for f in functions[:5]])}\n"
                
            return description
        except Exception as e:
            return f"Python file - Could not analyze: {str(e)}\n"
    
    def send_email_with_attachment(self, to_email, subject, body, attachment_path, custom_description=None):
        """
        Send email with attachment and automatic content description
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Generate file description
            if custom_description:
                file_description = custom_description
            else:
                file_description = self.analyze_file_content(attachment_path)
            
            # Email body with file description
            email_body = f"{body}\n\n"
            email_body += "=" * 50 + "\n"
            email_body += "ATTACHMENT ANALYSIS:\n"
            email_body += "=" * 50 + "\n"
            email_body += file_description
            
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Add attachment
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()
            
            logging.info(f"Email sent successfully to {to_email} with attachment {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_bulk_emails(self, email_list, subject, body, attachments_folder):
        """
        Send emails to multiple recipients with attachments from a folder
        """
        if not os.path.exists(attachments_folder):
            logging.error(f"Attachments folder does not exist: {attachments_folder}")
            return
        
        attachment_files = [f for f in os.listdir(attachments_folder) 
                          if os.path.isfile(os.path.join(attachments_folder, f))]
        
        if not attachment_files:
            logging.warning(f"No files found in attachments folder: {attachments_folder}")
            return
        
        successful_sends = 0
        failed_sends = 0
        
        for email in email_list:
            for filename in attachment_files:
                file_path = os.path.join(attachments_folder, filename)
                email_subject = f"{subject} - {filename}"
                
                if self.send_email_with_attachment(email, email_subject, body, file_path):
                    successful_sends += 1
                else:
                    failed_sends += 1
        
        logging.info(f"Bulk email complete. Successful: {successful_sends}, Failed: {failed_sends}")

def main():
    """
    Example usage of the email automation system
    """
    # Initialize email automation
    email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
    
    # Example 1: Send single email with attachment
    print("Email Automation System")
    print("=" * 50)
    
    # Get user input
    recipient_email = input("Enter recipient email address: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    attachment_path = input("Enter path to attachment file: ")
    
    if os.path.exists(attachment_path):
        success = email_automation.send_email_with_attachment(
            to_email=recipient_email,
            subject=subject,
            body=body,
            attachment_path=attachment_path
        )
        
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email. Check the logs for details.")
    else:
        print("❌ Attachment file not found!")

if __name__ == "__main__":
    main()
