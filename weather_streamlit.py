import streamlit as st
import pandas as pd
import plotly.express as px


def generate_streamlit_data():
    df = pd.read_csv('test.csv')

    st.title("Mobile Dash")
    st.write("API Data Visualization")
    fig = px.scatter(df, x="time", y="temperature_2m")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="time", y="precipitation_probability")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(df, x="time", y="relative_humidity_2m")
    st.plotly_chart(fig3, use_container_width=True)


if __name__ == '__main__':
    generate_streamlit_data()