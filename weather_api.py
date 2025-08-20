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
    

def deco_print_and_log(msg):
    """Logs message and if debug mode is enabled, prints to console."""
    def inner_deco(func):
        def wrapper(*args):
            msg_lst = [' - Begin', ' - End']

            _print_and_log(msg  + msg_lst[0])

            result = func(*args)

            _print_and_log(msg  + msg_lst[1])

            return result
        return wrapper
    return inner_deco


def _print_and_log(msg, logger=create_logger('__main__')):
    logger.info(msg)
    if debug_mode:
        print(_format_line(msg))


def _format_line(msg):
    """Adds a format line after each message."""
    format_line = '-----==========-----'
    return msg + '\n' + format_line


@deco_print_and_log('Download weather data')
def download_weather_data(url, run_time):
    """Downloads data from https://open-meteo.com API, creates file and returns dictionary."""

    try:
        result = requests.get(url)
    except:
        _print_and_log(Exception)   

    _print_and_log(f'Status code: {result.status_code}')

    _print_and_log('Saving source file - Begin')
    
    src_file = f'.\\output_files\\weather_file_{run_time}.json'

    try:
        with open(src_file, mode='a') as f:
            json.dump(result.json(), f, indent=4)
    except:
        _print_and_log(Exception)

    _print_and_log(f"Source file: {src_file}")
    _print_and_log('Saving source file - End')

    return json.loads(result.text)


@deco_print_and_log('Generate CSV and DataFrame')
def generate_csv_and_dataframe(input, run_time):
    """Generates csv and returns dataframe."""
    
    _print_and_log('    Saving destination file - Begin')
    dest_file = f".\\output_files\\output_file_{run_time}.csv"
    
    try:
        df = pd.DataFrame(input)
        df.to_csv(dest_file)
    except:
        _print_and_log(Exception)

    _print_and_log(f"   Destination file: {dest_file}")
    _print_and_log('    Saving destination file - End')
    
    return df
