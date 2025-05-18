Note: main code to monitoring the switches 


import os
import time
import platform
import smtplib
import threading
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load from .env

# Configuration
SWITCH_IPS = ["IP-1", "IP-2", "IP-3", "IP-4", "IP"]
CHECK_INTERVAL = 5   
switch_statuses = {ip: "Unknown" for ip in SWITCH_IPS}
last_alert_time = {}

app = Flask(__name__)

def ping(ip):
    """Cross-platform ping"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    return os.system(f"ping {param} 1 {ip} > /dev/null 2>&1")

def check_switches():
    while True:
        for ip in SWITCH_IPS:
            response = ping(ip)
            if response == 0:
                switch_statuses[ip] = "Online"
            else:
                switch_statuses[ip] = "Offline"
                send_email_alert(ip)
        time.sleep(CHECK_INTERVAL)

def send_email_alert(switch_ip):
    import smtplib

    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(',')

    now = time.time()
    if switch_ip in last_alert_time and now - last_alert_time[switch_ip] < 300:
        return
    last_alert_time[switch_ip] = now

    try:
        subject = f"Alert: Switch {switch_ip} is DOWN!"
        body = f"Switch with IP {switch_ip} is not responding."
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            for email in ADMIN_EMAILS:
                server.sendmail(EMAIL_SENDER, email.strip(), message)

        print(f"[INFO] Alert sent for {switch_ip}")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(switch_statuses)

if __name__ == "__main__":
    thread = threading.Thread(target=check_switches, daemon=True)
    thread.start()
    app.run(debug=True, host="0.0.0.0", port=5000)

