import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function untuk menyiapkan data
def create_monthly_df(df):
    monthly_df = df.resample(rule='M', on='datetime').agg({
        "PM2.5": "mean"
    }).reset_index()
    return monthly_df

def create_yearly_df(df):
    yearly_df = df.groupby('year')['PM2.5'].mean().reset_index()
    return yearly_df

def create_hourly_df(df):
    hourly_df = df.groupby('hour')['PM2.5'].mean().reset_index()
    return hourly_df

# Load dataset
df = pd.read_csv("PRSA_Data_Dingling_20130301-20170228.csv")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df['PM2.5'].fillna(df['PM2.5'].mean(), inplace=True)

# Komponen Sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Air Quality: Dingling")
    
    # Filter Tahun
    start_year, end_year = st.slider(
        label='Rentang Tahun',
        min_value=2013,
        max_value=2017,
        value=(2013, 2017)
    )

main_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]

# Header
st.header('Dashboard Kualitas Udara Stasiun Dingling :cloud:')

# Pertanyaan 1: Tren Bulanan
st.subheader('Tren Bulanan PM2.5')
monthly_df = create_monthly_df(main_df)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(monthly_df["datetime"], monthly_df["PM2.5"], marker='o', linewidth=2, color="#90CAF9")
ax.set_title("Rata-rata Konsentrasi PM2.5 Bulanan", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
st.write("Insight: Terlihat pola musiman di mana polusi melonjak tajam pada awal tahun.")

# Pertanyaan 2 & 3: Perbandingan Tahun & Jam
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Tahunan")
    yearly_df = create_yearly_df(main_df)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=yearly_df, x='year', y='PM2.5', palette="viridis", ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Pola Harian (Jam)")
    hourly_df = create_hourly_df(main_df)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.lineplot(data=hourly_df, x='hour', y='PM2.5', marker='o', color="crimson", ax=ax)
    st.pyplot(fig)

# Analisis Lanjutan (Clustering)
st.subheader("Distribusi Kategori Kualitas Udara (Clustering)")
def categorize_aqi(pm_value):
    if pm_value <= 12: return 'Good'
    elif pm_value <= 35.4: return 'Moderate'
    elif pm_value <= 55.4: return 'Unhealthy for Sensitive Groups'
    elif pm_value <= 150.4: return 'Unhealthy'
    else: return 'Very Unhealthy'

main_df['AQI_Category'] = main_df['PM2.5'].apply(categorize_aqi)
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(data=main_df, x='AQI_Category', 
              order=['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy'],
              palette='magma', ax=ax)
st.pyplot(fig)
st.caption('Naufal Daffa Abdu Al Hafidl')