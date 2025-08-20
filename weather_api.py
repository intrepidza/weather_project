import requests
import json
import pandas as pd
import logging
from datetime import datetime
# from pathlib import Path
import os

debug_mode = True

def create_logger(logger_name):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='weather_log.log',
        filemode='a'
        )

    return logging.getLogger(logger_name)
    

def print_and_log(msg, logger=create_logger('__main__')):
    """Logs message and if debug mode is enabled, prints to console."""
    logger.info(msg)

    if debug_mode:
        print(_format_line(msg))


def _format_line(msg):
    """Adds a format line after each message."""
    format_line = '-----==========-----'
    return msg + '\n' + format_line


def download_weather_data(url, file_path, run_time):
    """Downloads data from https://open-meteo.com API, creates file and returns dictionary."""

    print_and_log('Downloading data - Begin')
    test = requests.get(url)
    print_and_log('Downloading data - End')

    print_and_log(f'Status code: {test.status_code}')

    print_and_log('Saving source file - Begin')
    with open(f'{file_path}\\output_files\\weather_file_{run_time}.json', mode='a') as f:
        json.dump(test.json(), f, indent=4)
    print_and_log('Saving source file - End')

    return json.loads(test.text)


def generate_csv_and_dataframe(input, file_path, run_time):
    """Generates csv and returns dataframe."""
    
    print_and_log('Saving destination file - Begin')
    df = pd.DataFrame(input)
    df.to_csv(f"{file_path}\\output_files\\output_file_{run_time}.csv")
    print_and_log('Saving destination file - Begin')
    
    return df
