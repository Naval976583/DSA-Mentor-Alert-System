from selenium import webdriver
import schedule
import time
from datetime import datetime, time as dt_time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from twilio.rest import Client
from flask import Flask, request, render_template

account_sid = 'AC5f69b50a8d521831e8ece53feaf6723d'
auth_token = '3f2037e2f4b1b38ed2d5e0a21320aeac'
twilio_phone_number = '+12566661039'
driver = webdriver.Chrome()

app = Flask(__name__)


class Details:
    recipient_phone_number = '+919112837969'
    email = 'naval976583@gmail.com'
    start_time = dt_time(20, 30)
    end_time = dt_time(22, 30)


@app.route("/login_page", methods=['POST', 'GET'])
def login_page():
    recipient_phone_number = request.form['phone']  # '+919112837969'
    Details.recipient_phone_number = recipient_phone_number
    Details.start_time = request.form["start_time"]
    Details.end_time = request.form["end_time"]
    driver.get('https://mentor.codingninjas.com/auth?redirect=%2Fdoubts%2Fworkplace')
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.presence_of_element_located((By.ID, 'phoneEmail')))
    email = request.form['email']  # 'naval976583@gmail.com'
    Details.email = email
    username.send_keys(email)

    continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit-buttons')))
    continue_button.click()
    return render_template("otp.html")


@app.route('/send_otp', methods=['POST', 'GET'])
def get_otp():
    otp = request.form["otp"]
    wait = WebDriverWait(driver, 10)
    otp_locate = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
    otp_locate.send_keys(otp)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
    login_button.click()

    toggle_switch = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mat-slide-toggle-thumb")))
    toggle_switch.click()
    return render_template("session.html")
    # doubt_notification_reminder()


@app.route("/doubt_reminder", methods=['POST', 'GET'])
def doubt_notification_reminder():
    t_1, t_2 = Details.start_time.split(":")
    t_3, t_4 = Details.end_time.split(":")
    start_time = dt_time(int(t_1), int(t_2))  # 8:30 PM
    end_time = dt_time(int(t_3), int(t_4))  # 10:30 PM
    current_time = datetime.now().time()
    wait = WebDriverWait(driver, 10)

    def my_task():
        if start_time <= current_time <= end_time:
            try:
                load_doubts = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "load-more-button-text")))
                load_doubts.click()

            except TimeoutException:
                try:
                    doubt_text = driver.find_element(By.CLASS_NAME, 'doubt-text')
                    message_body = "Coding Ninjas -  Doubt Available"
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        body=message_body,
                        from_=twilio_phone_number,
                        to=Details.recipient_phone_number
                    )
                    print('Doubt Available')
                except NoSuchElementException:
                    toggle_switch = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mat-slide-toggle-thumb")))
                    is_checked = toggle_switch.is_selected()
                    if not is_checked:
                        toggle_switch.click()

                    print('Error IN Locating Doubt')

    schedule.every().minute.do(my_task)

    while True:
        current_time = datetime.now().time()
        if current_time > end_time:
            driver.close()
            break
        schedule.run_pending()
        time.sleep(1)


@app.route("/", methods=['POST', 'GET'])
def login():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
