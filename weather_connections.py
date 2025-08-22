import os
from supabase import create_client
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

from weather_tools import deco_print_and_log, print_and_log

# Load environment variables from .env file
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL") or ""
supabase_key = os.getenv("SUPABASE_KEY") or ""
supabase_email = os.getenv("SUPABASE_EMAIL") or ""
supabase_pass = os.getenv("SUPABASE_PASS") or ""
gmail_email = os.getenv("APP_EMAIL") or ""
gmail_pass = os.getenv("APP_PASS") or ""

@deco_print_and_log("Connecting to Supabase")
def create_supabase_connection():
    try:
        supabase = create_client(supabase_url, supabase_key)

        user = supabase.auth.sign_in_with_password({
            "email": supabase_email,
            "password": supabase_pass
        })
    except Exception as e:
        print_and_log(f"Error connecting to Supabase: {e}")

    return supabase, user

@deco_print_and_log("Generating e-mail")
def create_email(mail={'Subject': 'Test Email','Content':'This is a test email.'}):
    msg = EmailMessage()
    msg["Subject"] = mail['Subject']
    msg['From'] = gmail_email
    msg['To'] = gmail_email
    msg.set_content(mail['Content'])  

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login((gmail_email or ""), (gmail_pass or "")) # gmail_email if gmail_email is not None else ""
        smtp.send_message(msg)

# create_email()
