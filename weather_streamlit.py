import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import time

from weather_connections import *


def generate_streamlit_data():
    # df = pd.read_csv('test.csv')

    try:
        supabase = create_supabase_connection()

        connect = supabase[0]
        user = supabase[1]

        response = (
            connect.table("test")
            .select("*")
            .execute()
        )

        df = pd.DataFrame(response.data)

    except Exception as e:
        print(f"Error when attempting to access Supabase or generate DataFrame: {e}")
        # sys.exit()

    st.title("Mobile Dash")
    st.write("API Data Visualization")

    # while len(df) == 0:
    #     time.sleep(5)

    cols = ['time','temperature_2m','rain','wind_direction_10m','wind_speed_10m','relative_humidity_2m','precipitation_probability','apparent_temperature','showers']
    df = df[cols]

    fig = px.scatter(df, x="time", y="temperature_2m")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="time", y="apparent_temperature")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(df, x="time", y="precipitation_probability")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(df, x="time", y="relative_humidity_2m")
    st.plotly_chart(fig4, use_container_width=True)


if __name__ == '__main__':
    generate_streamlit_data()