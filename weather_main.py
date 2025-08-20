import datetime
# import os
from pathlib import Path as p

from weather_api import *

@deco_print_and_log("App")
def main():
    # Variables:
    run_time = datetime.now().strftime('%H_%M_%S')
    url = 'https://api.open-meteo.com/v1/forecast?latitude=34.0757&longitude=18.8433&hourly=temperature_2m,rain,wind_direction_10m,wind_speed_10m,visibility,relative_humidity_2m'

    output = download_weather_data(url, run_time)
    df = generate_csv_and_dataframe(output, run_time)

    print(df.head(5))

if __name__ == '__main__':
    main()
