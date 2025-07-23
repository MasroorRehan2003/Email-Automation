"""
Example usage script for the Email Automation System
This script demonstrates different ways to use the email automation functionality
"""

from email_automation import EmailAutomation
import os

# Email configuration (same as in main script)
EMAIL_USER = 'i211707@nu.edu.pk'
EMAIL_PASS = 'uaosbqwpuemmioob'

def example_single_email():
    """Example: Send a single email with attachment"""
    print("=== Example 1: Single Email with Attachment ===")
    
    # Initialize email automation
    email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
    
    # Send email with attachment
    success = email_automation.send_email_with_attachment(
        to_email="recipient@example.com",  # Replace with actual recipient
        subject="Data Report - Monthly Analysis",
        body="Please find attached the monthly data analysis report.",
        attachment_path="./sample_data/sample.csv"  # Replace with actual file path
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email.")

def example_bulk_emails():
    """Example: Send bulk emails from attachments folder"""
    print("=== Example 2: Bulk Email from Folder ===")
    
    # Initialize email automation
    email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
    
    # List of recipients
    recipients = [
        "recipient1@example.com",
        "recipient2@example.com",
        "recipient3@example.com"
    ]
    
    # Send bulk emails
    email_automation.send_bulk_emails(
        email_list=recipients,
        subject="Weekly Data Updates",
        body="Please find attached your weekly data files.",
        attachments_folder="./attachments"  # Folder containing files to send
    )

def example_custom_description():
    """Example: Send email with custom file description"""
    print("=== Example 3: Email with Custom Description ===")
    
    # Initialize email automation
    email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
    
    custom_desc = """
    This file contains customer transaction data for Q4 2024.
    
    Data includes:
    - Customer IDs and names
    - Transaction amounts and dates
    - Product categories
    - Geographic information
    
    Please handle this data according to our privacy policy.
    """
    
    success = email_automation.send_email_with_attachment(
        to_email="manager@example.com",
        subject="Q4 Customer Data Report",
        body="Quarterly report as requested.",
        attachment_path="./data/q4_transactions.csv",
        custom_description=custom_desc
    )
    
    if success:
        print("✅ Email with custom description sent!")

def create_sample_files():
    """Create sample files for testing"""
    print("=== Creating Sample Files for Testing ===")
    
    # Create directories
    os.makedirs("sample_data", exist_ok=True)
    os.makedirs("attachments", exist_ok=True)
    
    # Create sample CSV
    import pandas as pd
    sample_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago'],
        'Salary': [50000, 75000, 60000]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_data/sample.csv', index=False)
    print("✅ Created sample.csv")
    
    # Create sample JSON
    import json
    sample_json = {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"}
        ],
        "settings": {
            "theme": "dark",
            "notifications": True
        }
    }
    with open('sample_data/config.json', 'w') as f:
        json.dump(sample_json, f, indent=2)
    print("✅ Created config.json")
    
    # Create sample text file
    with open('sample_data/notes.txt', 'w') as f:
        f.write("""This is a sample text file.
It contains multiple lines of text.
This can be used for testing the email automation system.

Features:
- Line counting
- Word counting
- Character counting
- Preview generation
""")
    print("✅ Created notes.txt")
    
    print("Sample files created successfully!")

if __name__ == "__main__":
    print("Email Automation System - Examples")
    print("=" * 50)
    
    # Create sample files first
    create_sample_files()
    
    print("\nChoose an example to run:")
    print("1. Single email with attachment")
    print("2. Bulk emails from folder")
    print("3. Email with custom description")
    print("4. Just analyze a file (no email)")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        example_single_email()
    elif choice == "2":
        example_bulk_emails()
    elif choice == "3":
        example_custom_description()
    elif choice == "4":
        # Just analyze files
        from email_automation import EmailAutomation
        email_automation = EmailAutomation(EMAIL_USER, EMAIL_PASS)
        
        print("\n=== File Analysis Only ===")
        file_path = input("Enter file path to analyze: ")
        if os.path.exists(file_path):
            analysis = email_automation.analyze_file_content(file_path)
            print("\nFile Analysis Result:")
            print("=" * 30)
            print(analysis)
        else:
            print("File not found!")
    else:
        print("Invalid choice!")
