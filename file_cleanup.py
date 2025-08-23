import os
from pathlib import Path
from datetime import datetime

from tools import deco_print_and_log, print_and_log

today = datetime.now().strftime('%Y_%m_%d')
root = Path.cwd()
news_file_pattern = "ai_output*_*.txt"


@deco_print_and_log("Remove old files")
def remove_old_files():
    all_expected = [
        news_file_pattern.replace('*', '', 1).replace('*', today),
        news_file_pattern.replace('*', '2', 1).replace('*', today)
    ]

    all_matching = list(root.glob(news_file_pattern))

    removal_list = []

    for x in all_matching:
        if x.name not in all_expected:
            removal_list.append(x.name)

    try:
        for x in removal_list:
            print_and_log(f"Removing file: {x}")
            os.remove(x)
    except Exception as e:
        print_and_log(f"Error when removing files: {x}")
