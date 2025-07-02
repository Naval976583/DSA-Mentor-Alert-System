import os
import time
from datetime import datetime, time as dt_time
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from twilio.rest import Client
import schedule
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration class with default values
class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    DEFAULT_RECIPIENT = os.getenv('DEFAULT_RECIPIENT')
    DEFAULT_EMAIL = os.getenv('DEFAULT_EMAIL')
    START_TIME = dt_time(20, 30)  # 8:30 PM
    END_TIME = dt_time(22, 30)   # 10:30 PM

class UserSession:
    def __init__(self):
        self.recipient_phone_number = Config.DEFAULT_RECIPIENT
        self.email = Config.DEFAULT_EMAIL
        self.start_time = Config.START_TIME
        self.end_time = Config.END_TIME
        self.driver = None

    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

user_session = UserSession()

@app.route("/login_page", methods=['POST', 'GET'])
def login_page():
    try:
        user_session.recipient_phone_number = request.form['phone']
        user_session.start_time = parse_time(request.form["start_time"])
        user_session.end_time = parse_time(request.form["end_time"])
        user_session.email = request.form['email']
        
        if not user_session.driver:
            user_session.init_driver()
            
        driver = user_session.driver
        driver.get('https://mentor.codingninjas.com/auth?redirect=%2Fdoubts%2Fworkplace')
        
        wait = WebDriverWait(driver, 10)
        username = wait.until(EC.presence_of_element_located((By.ID, 'phoneEmail')))
        username.send_keys(user_session.email)

        continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit-buttons')))
        continue_button.click()
        
        return render_template("otp.html")
    except Exception as e:
        return render_template("error.html", message=str(e)), 500

@app.route('/send_otp', methods=['POST', 'GET'])
def get_otp():
    try:
        otp = request.form["otp"]
        wait = WebDriverWait(user_session.driver, 10)
        
        otp_locate = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
        otp_locate.send_keys(otp)

        login_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Login')]")))
        login_button.click()

        toggle_switch = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "mat-slide-toggle-thumb")))
        toggle_switch.click()
        
        return render_template("session.html")
    except Exception as e:
        return render_template("error.html", message=str(e)), 500

@app.route("/doubt_reminder", methods=['POST', 'GET'])
def doubt_notification_reminder():
    try:
        current_time = datetime.now().time()
        wait = WebDriverWait(user_session.driver, 10)

        def check_for_doubts():
            nonlocal current_time
            current_time = datetime.now().time()
            
            if user_session.start_time <= current_time <= user_session.end_time:
                try:
                    load_doubts = wait.until(EC.element_to_be_clickable(
                        (By.CLASS_NAME, "load-more-button-text")))
                    load_doubts.click()
                except TimeoutException:
                    try:
                        driver.find_element(By.CLASS_NAME, 'doubt-text')
                        send_notification("Coding Ninjas - Doubt Available")
                    except NoSuchElementException:
                        toggle_switch = wait.until(EC.element_to_be_clickable(
                            (By.CLASS_NAME, "mat-slide-toggle-thumb")))
                        if not toggle_switch.is_selected():
                            toggle_switch.click()

        schedule.every().minute.do(check_for_doubts)

        while current_time <= user_session.end_time:
            schedule.run_pending()
            time.sleep(1)
            current_time = datetime.now().time()

        user_session.close_driver()
        return "Session ended", 200
        
    except Exception as e:
        user_session.close_driver()
        return render_template("error.html", message=str(e)), 500

@app.route("/", methods=['POST', 'GET'])
def login():
    return render_template("index.html")

def send_notification(message):
    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=Config.TWILIO_PHONE_NUMBER,
        to=user_session.recipient_phone_number
    )

def parse_time(time_str):
    """Parse time string in HH:MM format to time object"""
    hours, minutes = map(int, time_str.split(':'))
    return dt_time(hours, minutes)

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
