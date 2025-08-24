import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

from interface import *

# Streamlit config:
st.set_page_config(layout="wide")


def generate_streamlit_data():
    # today = datetime.now().strftime('%Y_%m_%d')

    # file_name1 = f'news_{today}.txt'
    # file_name2 = f'news2_{today}.txt'

    # root_path = Path.cwd() / 'output_files/news/'

    # check_path1 = root_path / file_name1
    # check_path2 = root_path / file_name2

    try:
        supabase = create_supabase_connection()

        connect = supabase[0]
        user = supabase[1]

        response_weather = (
            connect.table("weather")
            .select("*")
            .execute()
        )

        response_news = (
            connect.table("news")
            .select("*")
            .execute()
        )

        df = pd.DataFrame(response_weather.data)
        df_news = pd.DataFrame(response_news.data)

    except Exception as e:
        print(f"Error when attempting to access Supabase or generate DataFrame: {e}")

    st.title("News and Weather Dash")

    # col1, col2 = st.columns(2)
    
    # with col1:
    st.image('assets//logo.png', width=300)
    
    # with col2:
        

    # if check_path1.exists() and check_path2.exists():
    st.write("News:")

    st.caption("US")
    # col1, col2 = st.columns(2)

    # # with open(check_path1, encoding='utf-8') as f1:
    # with open(check_path1) as f1:
    #     output1 = f1.read()

    # # with open(check_path2, encoding='utf-8') as f2:
    # with open(check_path2) as f2:
    #     output2 = f2.read() 

    # lines1 = output1.splitlines()
    # lines2 = output2.splitlines()

    df1 = df_news[df_news['country']=='US'][['content', 'link']]
    df2 = df_news[df_news['country']=='ZA'][['content', 'link']]

    # df1 = pd.DataFrame(lines1, columns=["World News"])
    # df2 = pd.DataFrame(lines2, columns=["SA News"])

    # with col1:
    st.dataframe(df1, hide_index=True, row_height=100)

    st.caption("ZA")

    # with col2:
    st.dataframe(df2, hide_index=True, row_height=100)

######

    st.image('assets//logo2.png', width=300)

    st.write("Weather:")

    cols = ['time','temperature','rain','wind_direction','wind_speed','relative_humidity','precipitation_probability','apparent_temperature','showers']
    df = df[cols]

    fig = px.scatter(df, x="time", y="temperature")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="time", y="apparent_temperature")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(df, x="time", y="precipitation_probability")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(df, x="time", y="relative_humidity")
    st.plotly_chart(fig4, use_container_width=True)


if __name__ == '__main__':
    generate_streamlit_data()