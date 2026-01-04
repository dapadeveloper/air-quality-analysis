import streamlit as st
import pandas as pd

df = pd.read_csv("PRSA_Data_Huairou_20130301-20170228.csv")

df['date'] = pd.to_datetime(df[['year','month','day','hour']])

st.title("Dashboard Kualitas Udara – Stasiun Huairou")

start = st.date_input("Mulai", df['date'].min())
end = st.date_input("Selesai", df['date'].max())

filtered = df[(df['date'] >= pd.to_datetime(start)) & (df['date'] <= pd.to_datetime(end))]

st.line_chart(filtered.groupby(filtered['date'].dt.date)['PM2.5'].mean())

st.bar_chart(filtered.groupby('hour')['PM2.5'].mean())
