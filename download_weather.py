import requests
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils import *

today = datetime.now().strftime('%Y_%m_%d')

@deco_print_and_log('Download weather data')
def download_weather_data(url):
    """Downloads data from https://open-meteo.com API, creates file and returns dictionary."""

    try:
        result = requests.get(url)
        result.raise_for_status()
    except Exception as e:
        print_and_log(f"error downloading data: {e}")
 
    print_and_log(f'Status code: {result.status_code}')

    print_and_log('Saving source file - Begin')
    
    src_file = f'.\\output_files\\weather\\weather_file_{today}.json'

    try:
        with open(src_file, mode='w') as f:
            json.dump(result.json(), f, indent=4)
    except Exception as e:
        print_and_log(f'Error when generating file: {e}')

    print_and_log(f"Source file: {src_file}")
    print_and_log('Saving source file - End')

    return json.loads(result.text)


@deco_print_and_log('Generate CSV and DataFrame')
def generate_csv_and_dataframe(input=None):
    """Generates csv and returns dataframe."""

    if not input: # Get latest available file: 
        output_dir = Path.cwd() / "output_files/weather/"
        files_by_pattern = output_dir.glob('weather_file_*')
        file_path = max(files_by_pattern, key=lambda f: f.stat().st_mtime)

        with open(file_path) as f:
            input = json.load(f)

    dest_file = f".\\output_files\\weather\\output_file_{today}.csv" 
    
    try:
        df = pd.DataFrame(input["hourly"], columns=input["hourly_units"])

        # Add scalar metadata to every row
        for k, v in input.items():
            if k not in ["hourly", "hourly_units"]:  # exclude list-style fields
                df[k] = v

        cols = [
            'time',
            'temperature_2m',
            'rain',
            'wind_direction_10m',
            'wind_speed_10m',
            'relative_humidity_2m',
            'precipitation_probability',
            'apparent_temperature',
            'showers',
            ]

        df = df[cols]

        df.rename(columns={
            'temperature_2m':'temperature',
            'wind_direction_10m':'wind_direction',
            'wind_speed_10m':'wind_speed',
            'relative_humidity_2m':'relative_humidity',
            }
            ,inplace=True
        )
        
        df.to_csv(dest_file, index=False)

        return df

    except Exception as e:
        print_and_log(f"Error when generating Dataframe or file {dest_file}: {e}")

    return df
