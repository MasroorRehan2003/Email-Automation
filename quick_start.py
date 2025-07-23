#!/usr/bin/env python3
"""
Quick Start Script for Email Automation System
This script provides an easy way to send a single email with attachment analysis
"""

from email_automation import EmailAutomation
import os
import sys

def main():
    print("=" * 60)
    print("🚀 EMAIL AUTOMATION SYSTEM - QUICK START")
    print("=" * 60)
    
    # Email configuration (already set with your credentials)
    EMAIL_USER = 'i211707@nu.edu.pk'
    EMAIL_PASS = 'uaosbqwpuemmioob'
    
    print(f"✉️  Sender Email: {EMAIL_USER}")
    print()
    
    # Get user input
    try:
        recipient = input("📧 Enter recipient email address: ").strip()
        if not recipient:
            print("❌ No recipient provided!")
            return
            
        subject = input("📝 Enter email subject: ").strip()
        if not subject:
            subject = "Automated Email with File Analysis"
            
        body = input("💬 Enter email message: ").strip()
        if not body:
            body = "Please find the attached file with automated analysis."
            
        attachment_path = input("📎 Enter path to attachment file: ").strip()
        if not attachment_path:
            print("❌ No attachment file provided!")
            return
            
        if not os.path.exists(attachment_path):
            print(f"❌ File not found: {attachment_path}")
            return
            
        # Initialize email automation
        print("\n🔧 Initializing email system...")
        email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
        
        # Send email
        print("📤 Sending email...")
        success = email_automation.send_email_with_attachment(
            to_email=recipient,
            subject=subject,
            body=body,
            attachment_path=attachment_path
        )
        
        if success:
            print("✅ Email sent successfully!")
            print(f"   → To: {recipient}")
            print(f"   → Subject: {subject}")
            print(f"   → Attachment: {os.path.basename(attachment_path)}")
        else:
            print("❌ Failed to send email!")
            print("   Check the logs for details.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
