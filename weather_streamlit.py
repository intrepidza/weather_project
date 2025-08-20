import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("test.csv")

st.title("Mobile Dash")
st.write("API Data Visualization")
fig = px.scatter(df, x="time", y="temperature_2m")
st.plotly_chart(fig, use_container_width=True)
