from datetime import datetime

from download_news import generate_news_data
from download_weather import download_weather_data, generate_csv_and_dataframe
from file_cleanup import remove_old_files
from interface import create_email, load_into_supabase
# from weather_reader import read_and_process
from utils import deco_print_and_log, print_and_log

print('-----==========-----')

@deco_print_and_log("App")
def main():
    # run_time = datetime.now().strftime('%H_%M_%S')
    url = 'https://api.open-meteo.com/v1/forecast?latitude=-34.084&longitude=18.8211&hourly=temperature_2m,rain,wind_direction_10m,wind_speed_10m,visibility,relative_humidity_2m,precipitation_probability,apparent_temperature,showers'

    try:
        news_output = generate_news_data()

        load_into_supabase('news', news_output[0])

        load_into_supabase('news', news_output[1])

        output = download_weather_data(url)

        data = generate_csv_and_dataframe(output)

        load_into_supabase('weather', data)

        remove_old_files()

        create_email(
                    {
                        'Subject': 'App run completed',
                        'Content':'All App processes have finished running. \n\nReview at: https://intrepidza-weather-project-weather-streamlit-bci1hz.streamlit.app'
                    }
        )
       
    except Exception as e:
        print_and_log(e)    
    

if __name__ == '__main__':
    main()
