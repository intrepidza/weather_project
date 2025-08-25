import os
from supabase import create_client
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import pandas as pd
from pathlib import Path

from utils import deco_print_and_log, print_and_log

# Load environment variables from .env file
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL") or ""
supabase_key = os.getenv("SUPABASE_KEY") or ""
supabase_email = os.getenv("SUPABASE_EMAIL") or ""
supabase_pass = os.getenv("SUPABASE_PASS") or ""
gmail_email = os.getenv("APP_EMAIL") or ""
gmail_pass = os.getenv("APP_PASS") or ""

@deco_print_and_log("Create Supabase Connection")
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


@deco_print_and_log("Load data into Supabase")
def load_into_supabase(table, df=None):
    # Establish Supabase connection
    supabase = create_supabase_connection()
    connect = supabase[0]
    user = supabase[1]

    # if df is None: # Get latest available file: 
    #     output_dir = Path.cwd() / "output_files/weather/"
    #     files_by_pattern = output_dir.glob('output_file*')
    #     file_path = max(files_by_pattern, key=lambda f: f.stat().st_mtime)

    #     # with open(file_path) as f:
    #     df = pd.read_csv(file_path)


    df['user_id'] = user.user.id
    data = df.to_dict(orient='records')
    

    print_and_log(f"Removing old {table} data.")
    try:
        response = connect.rpc(f"truncate_{table}").execute()
    except Exception as e:
        print_and_log(f"Error when attempting to remove old {table} data {e}")

    # data = [{'time': '2025-08-23 00:00:00', 
    # 'temperature': 12.0, 
    # 'rain': 0.0, 
    # 'wind_direction': 358, 
    # 'wind_speed': 12.2, 
    # 'relative_humidity': 88, 
    # 'precipitation_probability': 15, 
    # 'apparent_temperature': 10.3, 
    # 'showers': 0.0, 
    # 'user_id': '2db06982-a559-4034-b709-eb8f0c4ceed7'
    # }]

    try:
        response = connect.table(table).insert(data).execute()
    except Exception as e:
        print_and_log(f"Error when attempting to insert data into {table} table: {e}")

    connect.auth.sign_out()

# load_into_supabase('news')


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
