"""
Test script for Email Automation System
Tests various components without sending actual emails
"""

import os
import sys
import json
import pandas as pd
from email_automation import EmailAutomation

def test_file_analysis():
    """Test file analysis capabilities"""
    print("=== Testing File Analysis ===")
    
    # Create test files
    os.makedirs("test_files", exist_ok=True)
    
    # Test CSV
    test_data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
    df = pd.DataFrame(test_data)
    df.to_csv('test_files/test.csv', index=False)
    
    # Test JSON
    test_json = {'users': [{'id': 1, 'name': 'Alice'}]}
    with open('test_files/test.json', 'w') as f:
        json.dump(test_json, f)
    
    # Test text file
    with open('test_files/test.txt', 'w') as f:
        f.write("This is a test file.\nIt has multiple lines.\nFor testing purposes.")
    
    # Test analysis
    email_automation = EmailAutomation('test@example.com', 'test_password')
    
    test_files = ['test_files/test.csv', 'test_files/test.json', 'test_files/test.txt']
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n--- Analyzing {file_path} ---")
            analysis = email_automation.analyze_file_content(file_path)
            print(analysis)
            print("✅ Analysis successful")
        else:
            print(f"❌ File not found: {file_path}")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_files")
    print("\n✅ File analysis tests completed")

def test_email_configuration():
    """Test email configuration"""
    print("\n=== Testing Email Configuration ===")
    
    try:
        from config import EMAIL_CONFIG, EMAIL_TEMPLATES, SUPPORTED_EXTENSIONS
        
        print("✅ Configuration imported successfully")
        print(f"Email user: {EMAIL_CONFIG['EMAIL_USER']}")
        print(f"SMTP server: {EMAIL_CONFIG['SMTP_SERVER']}")
        print(f"Available templates: {list(EMAIL_TEMPLATES.keys())}")
        print(f"Supported extensions: {len(sum(SUPPORTED_EXTENSIONS.values(), []))}")
        
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")

def test_class_initialization():
    """Test class initialization"""
    print("\n=== Testing Class Initialization ===")
    
    try:
        # Test basic class
        email_automation = EmailAutomation('test@example.com', 'test_password')
        print("✅ EmailAutomation class initialized")
        
        # Test advanced class
        from advanced_automation import AdvancedEmailAutomation
        advanced_automation = AdvancedEmailAutomation()
        print("✅ AdvancedEmailAutomation class initialized")
        
    except Exception as e:
        print(f"❌ Class initialization failed: {e}")

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n=== Testing Dependencies ===")
    
    required_packages = [
        'pandas',
        'openpyxl', 
        'schedule',
        'pathlib',
        'json',
        'smtplib',
        'email'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'pathlib':
                from pathlib import Path
            elif package == 'openpyxl':
                import openpyxl
            elif package == 'schedule':
                import schedule
            elif package == 'pandas':
                import pandas
            elif package == 'json':
                import json
            elif package == 'smtplib':
                import smtplib
            elif package == 'email':
                import email
            
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {missing_packages}")
        print("Install with: pip install -r requirements.txt")
    else:
        print("\n✅ All dependencies are installed")

def main():
    """Run all tests"""
    print("Email Automation System - Test Suite")
    print("=" * 50)
    
    test_dependencies()
    test_email_configuration() 
    test_class_initialization()
    test_file_analysis()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("\nTo send actual emails, update the email credentials in config.py")
    print("and run: python email_automation.py")

if __name__ == "__main__":
    main()
