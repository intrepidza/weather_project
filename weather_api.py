import requests
import json
import pandas as pd
from datetime import datetime

from weather_tools import *


@deco_print_and_log('Download weather data')
def download_weather_data(url, run_time):
    """Downloads data from https://open-meteo.com API, creates file and returns dictionary."""

    try:
        result = requests.get(url)
        result.raise_for_status()
    except Exception as e:
        print_and_log(f"error downloading data: {e}")
 
    print_and_log(f'Status code: {result.status_code}')

    print_and_log('Saving source file - Begin')
    
    src_file = f'.\\output_files\\weather_file_{run_time}.json'

    try:
        with open(src_file, mode='w') as f:
            json.dump(result.json(), f, indent=4)
    except Exception as e:
        print_and_log(e)

    print_and_log(f"Source file: {src_file}")
    print_and_log('Saving source file - End')

    return json.loads(result.text)


@deco_print_and_log('Generate CSV and DataFrame')
def generate_csv_and_dataframe(input, run_time):
    """Generates csv and returns dataframe."""
    
    print_and_log('Saving destination file - Begin')
    dest_file = f".\\output_files\\output_file_{run_time}.csv"
    
    try:
        df = pd.DataFrame(input["hourly"], columns=input["hourly_units"])

        # Add scalar metadata to every row
        for k, v in input.items():
            if k not in ["hourly", "hourly_units"]:  # exclude list-style fields
                df[k] = v

        df.to_csv(dest_file)
    except Exception as e:
        print_and_log(f"Error when generating Dataframe or file {e}")

    print_and_log(f"Destination file: {dest_file}")
    print_and_log('Saving destination file - End')
    
    return df
