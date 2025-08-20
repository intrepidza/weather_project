import pandas as pd
from pathlib import Path as p
from weather_tools import *


@deco_print_and_log("Read latest Dataframe CSV and format")
def read_and_process(file=None):
    if not file:    # Get latest available file:
        cur_dir = p.cwd()
        output_dir = cur_dir / "output_files"
        files_by_pattern = output_dir.glob('output_file_*')
        file = max(files_by_pattern, key=lambda f: f.stat().st_mtime)

    try:
        df = pd.read_csv(file, encoding='utf-8')
        df['time'] = pd.to_datetime(df['time'])
        df.to_csv('test.csv')
    except Exception as e:
        print_and_log('Issue reading or generating file: {e}')
