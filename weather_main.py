import datetime
import os

from weather_api import *

# from .weather_api import print_and_log
# from .weather_api import download_weather_data
# from .weather_api import generate_csv_and_dataframe


def main():
    # Variables:
    run_time = datetime.now().strftime('%H_%M_%S')
    file_path = os.path.abspath('.')
    url = 'https://api.open-meteo.com/v1/forecast?latitude=34.0757&longitude=18.8433&hourly=temperature_2m,rain,wind_direction_10m,wind_speed_10m,visibility,relative_humidity_2m'

    print_and_log('Starting App'.center(20, '-'))

    output = download_weather_data(url, file_path, run_time)

    df = generate_csv_and_dataframe(output, file_path, run_time)
    
    print(df.head(5))

    print_and_log('App completed'.center(20, '-'))



if __name__ == '__main__':
    main()
