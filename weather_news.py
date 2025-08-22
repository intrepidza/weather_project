import sys
from pathlib import Path
# from google import genai
# from groq import Groq
from datetime import datetime
from dotenv import load_dotenv
import os
import json

import requests

from weather_tools import deco_print_and_log, print_and_log


load_dotenv()


today = datetime.now().strftime('%Y_%m_%d')

file_name1 = f'ai_output_{today}.txt'
file_name2 = f'ai_output2_{today}.txt'

root_path = Path.cwd() #/ 'output_files/'

check_path1 = root_path / file_name1
check_path2 = root_path / file_name2


"""NewsData IO Testing:"""

api_key=os.environ.get("NEWSDATA_IO_API")

@deco_print_and_log("Generating news data")
def generate_news_data():
    
    if check_path1.exists():
        pass
    else:
        # US data:
        url = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=us"
        response = requests.get(url)

        with open('us_news_dump.txt','w') as f:
            json.dump(response.json().get("results", []), f, indent=4)

        with open(f'ai_output_{today}.txt','w') as f:
            try:
                for article in response.json().get("results", []):
                    if any(cat in (article['category'] or []) for cat in ['sports']):
                        continue

                    if any(cat in (article['creator'] or []) for cat in ["Sponsored Post"]):
                        continue

                    else:
                        f.write(f"* Title: {article['title']} * - * Article: {article['description']} * - * Published: {article['pubDate']} * - * Link: {article['link']} *\n")

            except Exception as e:
                print_and_log(f"Error! {e}")
    
    if check_path2.exists():
        pass
    else:
        # SA data:
        url2 = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=za"
        response2 = requests.get(url2)

        with open('sa_news_dump.txt','w') as f:
            json.dump(response2.json().get("results", []), f, indent=4)
        

        with open(f'ai_output2_{today}.txt','w') as f:
            try:
                for article in response2.json().get("results", []):
                    # if 'sports' in article['category'] or 'lotto' in article['category']:
                    
                    if any(cat in (article['category'] or []) for cat in ['sports']):
                        continue

                    if any(cat in (article['creator'] or []) for cat in ["Sponsored Post"]):
                        continue

                    else:
                        f.write(f"* Title: {article['title']} * - * Article: {article['description']} * - * Published: {article['pubDate']} * - * Link: {article['link']} *\n")

            except Exception as e:
                print_and_log(f"Error! {e}")

"""NewsData IO Testing:"""

# generate_news_data()

# response.json()

"""News API Testing

# api_key=os.environ.get("NEWS_API")

# url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
# response = requests.get(url)

# articles = response.json().get("articles", [])

# test = json.loads(response.request)

# url2 = f"https://newsapi.org/v2/top-headlines?country=za&apiKey={api_key}"
# response2 = requests.get(url2)

# articles2 = response2.json().get("articles", [])

# with open('news_dump.txt', 'w') as f:
#     # f.write(articles)
#     json.dump(articles, f, indent=4)



# US data:
# with open('ai_output_2025_08_21.txt','w') as f:
#     try:
#         for article in articles:
#             # f.write(f"**{article['title']}**\n")
#             # f.write(f"{article['description']}\n")
#             # # f.write(f"[Read more]({article['url']})\n")
#             # f.write(f"Published: {article['publishedAt']}\n")
#             f.write(f"* Title: {article['title']}** - Article:{article['description']} - Published: {article['publishedAt']}\n")

#     except Exception as e:
#         print("Error! {e}")

# # ZA data:

# with open('ai_output2_2025_08_21.txt','w') as f:
#     try:
#         for article in articles2:
#             # f.write(f"**{article['title']}**\n")
#             # f.write(f"{article['description']}\n")
#             # # f.write(f"[Read more]({article['url']})\n")
#             # f.write(f"Published: {article['publishedAt']}\n")
#             f.write(f"* Title: {article['title']}** - Article:{article['description']} - Published: {article['publishedAt']}\n")

#     except Exception as e:
#         print("Error! {e}")

# for article in articles:
#     print(article)
    # st.write(f"**{article['title']}**")
    # st.write(article['description'])
    # st.write(f"[Read more]({article['url']})")
    # st.write(f"Published: {article['publishedAt']}")

News API Testing"""



"""Gemini API testing 
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client()

# response1 = client.models.generate_content(
#     model="gemini-2.5-flash", 
#     contents="Give me a bullet-form output of the latest available biggest news in the world today. No need for a disclaimer, just the bullet-points."
# )

# response2 = client.models.generate_content(
#     model="gemini-2.5-flash", 
#     contents="Give me a bullet-form output of the latest available biggest news in South Africa today. No need for a disclaimer, just the bullet-points."
# )
"""

"""Groq API testing
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# chat_completion1 = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Give me a bullet-form output of the latest available biggest news in the world today. No need for a disclaimer, just the bullet-points.",
#         }
#     ],
#     # model="llama-3.3-70b-versatile",
#     model="compound-beta-mini",
# )

# chat_completion2 = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Give me a bullet-form output of the latest available biggest news in South Africa today. No need for a disclaimer, just the bullet-points.",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion1.choices[0].message.content)

# print(type(chat_completion))
# print(chat_completion)

# print(response1.text)
# print(response2.text)

# with open(check_path1,'w') as f:
#     f.write(str(chat_completion1.choices[0].message.content))

# with open(check_path2,'w') as f:
#     f.write(str(chat_completion2.choices[0].message.content))
"""
