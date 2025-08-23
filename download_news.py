from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import pandas as pd

import requests

from tools import deco_print_and_log, print_and_log


load_dotenv()


today = datetime.now().strftime('%Y_%m_%d')

file_name1 = f'news_{today}.txt'
file_name2 = f'news2_{today}.txt'

root_path = Path.cwd() / 'output_files/news/'

check_path1 = root_path / file_name1
check_path2 = root_path / file_name2


api_key=os.environ.get("NEWSDATA_IO_API")

@deco_print_and_log("Generating news data")
def generate_news_data():

    records = []
    records2 = []

    reference_keys = ['country', 'title', 'description', 'pubDate', 'link']

    
    if check_path1.exists():
        pass
    else:
        # US data:
        url = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=us"
        response = requests.get(url)

        # Keep copy of json
        with open(f'{root_path}/us_news_{today}.json','w', encoding='utf-8') as f:
            json.dump(response.json().get("results", []), f, indent=4)

        with open(check_path1,'w', encoding='utf-8') as f:
            try:
                for article in response.json().get("results", []):

                    article['country'] = 'US'

                    if any(cat in (article['category'] or []) for cat in ['sports']):
                        continue

                    if any(cat in (article['creator'] or []) for cat in ["Sponsored Post"]):
                        continue

                    else:
                        # record = f"* {article['country']}, Title: {article['title']} * - * Article: {article['description']} * - * Published: {article['pubDate']} *, * Link: {article['link']} *\n" 
                        
                        new_dict = {key: article[key] for key in reference_keys}

                        country, title, description, pubDate, link = new_dict.items()

                        record = dict(country = country[1], 
                                    content = f'* {title[0]}: {title[1]} * - * {description[0]}: {description[1]} * - * {pubDate[0]}: {pubDate[1]} *',
                                    link = link[1]
                        )
                        records.append(record)
                        f.write(f"{str(record)} /n")

            except Exception as e:
                print_and_log(f"Error! {e}")
    
    if check_path2.exists():
        pass
    else:
        # SA data:
        url2 = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=za"
        response2 = requests.get(url2)

        with open(f'{root_path}/sa_news_{today}.json','w', encoding='utf-8') as f:
            json.dump(response2.json().get("results", []), f, indent=4)
        

        with open(check_path2,'w', encoding='utf-8') as f:
            try:
                for article in response2.json().get("results", []):

                    article['country'] = 'ZA'
                   
                    if any(cat in (article['category'] or []) for cat in ['sports']):
                        continue

                    if any(cat in (article['creator'] or []) for cat in ["Sponsored Post"]):
                        continue

                    else:
                        # record2 = [{article['country']},{article['title']} * - * Article: {article['description']} * - * Published: {article['pubDate']} *, * Link: {article['link']} *\n" 
                        # record2 = f"* {article['country']}, Title: {article['title']} * - * Article: {article['description']} * - * Published: {article['pubDate']} *, * Link: {article['link']} *\n" 

                        new_dict = {key: article[key] for key in reference_keys}

                        country, title, description, pubDate, link = new_dict.items()

                        record2 = dict(country = country[1], 
                                    content = f'* {title[0]}: {title[1]} * - * {description[0]}: {description[1]} * - * {pubDate[0]}: {pubDate[1]} *',
                                    link = link[1]
                        )
                        records2.append(record2)
                        f.write(f"{str(record2)} /n")

            except Exception as e:
                print_and_log(f"Error! {e}")
    
    records = pd.DataFrame(records)
    records2 = pd.DataFrame(records2)

    return [records, records2]


if __name__ == '__main__':
    print(generate_news_data())
