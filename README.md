# Coding Ninjas Doubt Notifier

A Flask-based application that monitors Coding Ninjas mentor dashboard for new doubts and sends SMS notifications via Twilio when doubts are available during specified time windows.

## Features

- Automated login to Coding Ninjas mentor portal
- Real-time monitoring for new doubts
- SMS notifications via Twilio
- Configurable monitoring time windows
- Web interface for easy configuration

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.7+
- Chrome browser installed
- ChromeDriver (matching your Chrome version)
- Twilio account with SMS capabilities
- Coding Ninjas mentor account

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/coding-ninjas-doubt-notifier.git
   cd coding-ninjas-doubt-notifier
   
2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
  ```bash
  pip install -r requirements.txt

4. Create a .env file in the project root and configure it:
  ```ini
  TWILIO_ACCOUNT_SID=your_account_sid
  TWILIO_AUTH_TOKEN=your_auth_token
  TWILIO_PHONE_NUMBER=+12566661039
  DEFAULT_RECIPIENT=+919112837969
  DEFAULT_EMAIL=naval976583@gmail.com
  FLASK_DEBUG=True

## Usage
1. Run the application
  ```bash
    python app.py
2. Open your browser and navigate to:
  ```bash
    http://localhost:5000
3. Follow these steps in the web interface:

  Enter your Coding Ninjas login email
  
  Enter your phone number for notifications
  
  Set your preferred monitoring time window
  
  Click "Login" and follow the OTP verification process
  
  Start the monitoring session

4. Project Structure
  coding-ninjas-doubt-notifier/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
│   ├── index.html        # Login page
│   ├── otp.html          # OTP verification page
│   ├── session.html      # Monitoring session page
│   └── error.html        # Error page
└── README.md             # This file

## Configuration Options
All configuration is done through the .env file:

Variable	Description	Example
TWILIO_ACCOUNT_SID	Your Twilio account SID	AC5f69b50a8d5267831...
TWILIO_AUTH_TOKEN	Your Twilio auth token	3f2037hj2f4b1b38e...
TWILIO_PHONE_NUMBER	Your Twilio phone number	+12566661039
DEFAULT_RECIPIENT	Default phone number for notifications	+912813849697
DEFAULT_EMAIL	Default Coding Ninjas login email	abc@gmail.com
FLASK_DEBUG	Flask debug mode (True/False)	True

Troubleshooting
ChromeDriver issues:

Ensure ChromeDriver version matches your Chrome browser version

Add ChromeDriver to your PATH or specify its location in the code

Twilio SMS not working:

Verify your Twilio credentials are correct

Check your Twilio account has sufficient balance

Ensure the recipient number is verified (for trial accounts)

Login issues:

Double-check your Coding Ninjas credentials

Ensure you're using the correct OTP

Security Notes
Never commit your .env file to version control

Keep your Twilio credentials secret

The application stores session information in memory only

