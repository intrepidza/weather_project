import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_email = os.getenv("SUPABASE_EMAIL")
supabase_pass = os.getenv("SUPABASE_PASS")

def create_supabase_connection():
    supabase = create_client(supabase_url, supabase_key)

    user = supabase.auth.sign_in_with_password({
        "email": supabase_email,
        "password": supabase_pass
    })

    return supabase, user
