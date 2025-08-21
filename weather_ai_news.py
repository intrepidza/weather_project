import sys
from pathlib import Path
# from google import genai
from groq import Groq
from datetime import datetime
import os

today = datetime.now().strftime('%Y_%m_%d')

file_name1 = f'ai_output_{today}.txt'
file_name2 = f'ai_output2_{today}.txt'

root_path = Path.cwd() #/ 'output_files/'

check_path1 = root_path / file_name1
check_path2 = root_path / file_name2

# if check_path1.exists() or check_path2.exists():
#     sys.exit()

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

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion1 = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Give me a bullet-form output of the latest available biggest news in the world today. No need for a disclaimer, just the bullet-points.",
        }
    ],
    # model="llama-3.3-70b-versatile",
    model="compound-beta-mini",
)

chat_completion2 = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Give me a bullet-form output of the latest available biggest news in South Africa today. No need for a disclaimer, just the bullet-points.",
        }
    ],
    model="llama-3.3-70b-versatile",
)

# print(chat_completion1.choices[0].message.content)

# print(type(chat_completion))
# print(chat_completion)

# print(response1.text)
# print(response2.text)

with open(check_path1,'w') as f:
    f.write(str(chat_completion1.choices[0].message.content))

with open(check_path2,'w') as f:
    f.write(str(chat_completion2.choices[0].message.content))
