import pandas as pd
from pathlib import Path as p

from weather_connections import *
from weather_tools import *


@deco_print_and_log("Read latest Dataframe CSV and format")
def read_and_process(file=None):
    if not file:    # Get latest available file:
        cur_dir = p.cwd()
        output_dir = cur_dir / "output_files"
        files_by_pattern = output_dir.glob('output_file_*')
        file = max(files_by_pattern, key=lambda f: f.stat().st_mtime)

        print_and_log(f"Using file: {file}")

    try:
        df = pd.read_csv(file, encoding='utf-8')

        # Expected columns:
        cols = ['time','temperature_2m','rain','wind_direction_10m','wind_speed_10m','relative_humidity_2m','precipitation_probability','apparent_temperature','showers']
        # print(df[cols])
        df = df[cols]

        df['time'] = pd.to_datetime(df['time'])
        df.to_csv('test.csv', index=False)
    except Exception as e:
        print_and_log('Issue reading or generating file: {e}')


@deco_print_and_log("Load data into Supabase")
def load_into_supabase():
    supabase = create_supabase_connection()
    connect = supabase[0]
    user = supabase[1]

    df = pd.read_csv('test.csv')
    df['user_id'] = user.user.id
    data = df.to_dict(orient='records')

    # data = [{"test_int": 456, "test_text": "def", "user_id": user.user.id},{"test_int": 789, "test_text": "ghi", "user_id": user.user.id}]

    try:
        response = connect.table("test").insert(data).execute()
    except Exception as e:
        print(e)

    connect.auth.sign_out()

load_into_supabase()