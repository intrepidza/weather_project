from datetime import datetime

from download_news import generate_news_data
from download_weather import download_weather_data, generate_csv_and_dataframe
from file_cleanup import remove_old_files
from interface import create_email, load_into_supabase, create_supabase_connection, truncate_supabase_table
# from weather_reader import read_and_process
from utils import deco_print_and_log, print_and_log

print('-----==========-----')



@deco_print_and_log("App")
def main():
    # run_time = datetime.now().strftime('%H_%M_%S')
    url = 'https://api.open-meteo.com/v1/forecast?latitude=-34.084&longitude=18.8211&hourly=temperature_2m,rain,wind_direction_10m,wind_speed_10m,visibility,relative_humidity_2m,precipitation_probability,apparent_temperature,showers'

    try:
        connect, user = create_supabase_connection()

        news_output = generate_news_data()

        # news_output[0].to_csv('us_news_dump.txt')
        # news_output[1].to_csv('sa_news_dump.txt')

        truncate_supabase_table('news', connect)

        load_into_supabase('news', news_output[0], connect, user)

        load_into_supabase('news', news_output[1], connect, user)

        output = download_weather_data(url)

        data = generate_csv_and_dataframe(output)

        truncate_supabase_table('weather', connect)

        load_into_supabase('weather', data, connect, user)

        remove_old_files()

        create_email(
                    {
                        'Subject': 'App run completed',
                        'Content':'All App processes have finished running. \n\nReview at: https://newsandweatherproject.streamlit.app'
                    }
        )



        # Regenerate README.md file:
        readme_data = """
        This is a Weather API Github Project.

        Using it to experiment with.

        # Installation
        Used with Python version 3.11.4
        See requirements.txt file for packages.

        # Output
        https://newsandweatherproject.streamlit.app

        # TODO
        - Add e-mail event for drastic number changes
        - Fix truncation logic for news data
        - Testing
        """

        with open('README.md', 'w', encoding="utf-8") as f:
            f.write(readme_data)


    except Exception as e:
        print_and_log(e)    
    

if __name__ == '__main__':
    main()
