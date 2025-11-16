import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

QUERY = 'Senior Technical Support Engineer" ("8 years" OR "10 years" OR "8-12 years") (Bangalore OR Bengaluru OR Mysore OR Mysuru) jobs'

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 10
    }
    r = requests.get(url, params=params)
    return r.json()

def format_results(results):
    output = "Daily Job Search Results\n\n"
    for i, item in enumerate(results.get("items", []), start=1):
        output += f"{i}. {item.get('title')}\n{item.get('link')}\n{item.get('snippet','')}\n\n"
    return output

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Daily Senior Tech Support Job Results"
    msg["From"] = SMTP_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.sendmail(SMTP_EMAIL, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    results = google_search(QUERY)
    email_body = format_results(results)
    send_email(email_body)
    print("Email sent successfully!")
