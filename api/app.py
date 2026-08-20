import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates', static_folder='../static')

RECEIVING_EMAIL = "ieeeras.pesu.ecc.studentchapter@gmail.com"
GMAIL_USER = RECEIVING_EMAIL
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    srn = data.get('srn', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not all([name, srn, email, message]):
        return jsonify({"success": False, "error": "All fields are required."}), 400

    if not GMAIL_APP_PASSWORD:
        return jsonify({"success": False, "error": "Email is not configured on the server."}), 500

    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVING_EMAIL
    msg['Reply-To'] = email
    msg['Subject'] = f"IEEE RAS Website Contact — {name}"
    body = f"Name: {name}\nSRN: {srn}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECEIVING_EMAIL, msg.as_string())
        return jsonify({"success": True})
    except Exception as e:
        print("Email send error:", e)
        return jsonify({"success": False, "error": "Failed to send message. Try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
