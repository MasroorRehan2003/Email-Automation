# Email Automation System

An advanced email automation system that automatically sends emails with attachments and provides intelligent file content analysis.

## Features

- 🚀 **Automatic File Analysis**: Intelligently analyzes and describes different file types (CSV, Excel, JSON, Text, Python, etc.)
- 📧 **Smart Email Sending**: Sends emails with attachments and auto-generated content descriptions
- 📅 **Scheduling**: Schedule daily/weekly reports
- 📁 **Folder Monitoring**: Monitor folders for new files and send them automatically
- 🔄 **Bulk Processing**: Send multiple files to multiple recipients
- 📝 **Duplicate Prevention**: Tracks sent files to prevent duplicates
- 🎨 **Template System**: Customizable email templates
- 📊 **Logging**: Comprehensive logging and tracking

## Files Structure

```
├── email_automation.py      # Core email automation class
├── advanced_automation.py   # Advanced features (scheduling, monitoring)
├── example_usage.py        # Example usage demonstrations
├── config.py              # Configuration settings and templates
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Email Settings**:
   - Update your email credentials in `config.py`
   - For Gmail, you need to use an App Password (not your regular password)
   - Enable 2-factor authentication and generate an App Password

3. **Email Configuration**:
   ```python
   EMAIL_CONFIG = {
       'EMAIL_USER': 'your_email@gmail.com',
       'EMAIL_PASS': 'your_app_password',
       'SMTP_SERVER': 'smtp.gmail.com',
       'SMTP_PORT': 587
   }
   ```

## Usage Examples

### Basic Usage

```python
from email_automation import EmailAutomation

# Initialize
email_automation = EmailAutomation('your_email@gmail.com', 'your_app_password')

# Send single email with attachment
email_automation.send_email_with_attachment(
    to_email="recipient@example.com",
    subject="Data Report",
    body="Please find the attached report.",
    attachment_path="./data/report.csv"
)
```

### Advanced Usage

```python
from advanced_automation import AdvancedEmailAutomation

# Initialize advanced automation
automation = AdvancedEmailAutomation()

# Send new files from folder (prevents duplicates)
automation.send_new_files_from_folder(
    folder_path="./reports",
    recipients=["user1@example.com", "user2@example.com"],
    template="DATA_REPORT"
)

# Schedule daily reports
automation.schedule_daily_reports(
    folder_path="./daily_reports",
    recipients=["manager@example.com"],
    time_str="09:00"
)

# Monitor folder for new files
automation.monitor_folder_for_new_files(
    folder_path="./incoming",
    recipients=["team@example.com"],
    check_interval=300  # Check every 5 minutes
)
```

## File Analysis Capabilities

The system automatically analyzes and describes:

- **CSV Files**: Row/column counts, column names, data types
- **Excel Files**: Sheet analysis, data structure
- **JSON Files**: Object structure, keys, data types
- **Text Files**: Line/word counts, preview content
- **Python Files**: Functions, classes, imports analysis
- **Images**: File type and basic info
- **PDFs**: Document type recognition

## Running the Examples

1. **Basic Examples**:
   ```bash
   python example_usage.py
   ```

2. **Advanced Features**:
   ```bash
   python advanced_automation.py
   ```

3. **Interactive Mode**:
   ```bash
   python email_automation.py
   ```

## Email Templates

The system includes predefined templates:

- `DATA_REPORT`: For data analysis reports
- `WEEKLY_UPDATE`: For weekly updates
- `CUSTOM`: General purpose template

Templates can be customized in `config.py`.

## Security Notes

- Use Gmail App Passwords instead of regular passwords
- Keep your credentials secure and don't commit them to version control
- Consider using environment variables for production deployments

## Logging

All email activities are logged to:
- Console output
- `email_automation.log` file
- `sent_files.json` for tracking sent files

## Troubleshooting

### Common Issues:

1. **Authentication Error**: 
   - Ensure you're using Gmail App Password
   - Enable 2-factor authentication

2. **File Not Found**:
   - Check file paths are correct
   - Ensure files exist before sending

3. **SMTP Connection Error**:
   - Check internet connection
   - Verify SMTP settings

### Debug Mode:

Enable detailed logging by setting log level to DEBUG in `config.py`:

```python
LOGGING_CONFIG = {
    'level': 'DEBUG',
    # ... other settings
}
```

## License

This project is open source and available under the MIT License.
