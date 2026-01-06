import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn
sns.set(style='dark')

# Mendapatkan path absolut dari folder tempat dashboard.py berada
current_dir = os.path.dirname(os.path.abspath(__file__))
# Menggabungkan path folder dengan nama file data
file_path = os.path.join(current_dir, "all_data.csv")

# --- Helper Functions ---
def create_monthly_df(df):
    monthly_df = df.resample(rule='M', on='datetime').agg({
        "PM2.5": "mean"
    }).reset_index()
    return monthly_df

def create_yearly_df(df):
    return df.groupby('year')['PM2.5'].mean().reset_index()

def create_hourly_df(df):
    return df.groupby('hour')['PM2.5'].mean().reset_index()

# --- Load Dataset dengan Error Handling ---
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
else:
    st.error(f"File tidak ditemukan di: {file_path}. Pastikan 'all_data.csv' ada di folder yang sama dengan dashboard.py.")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Air Quality: Dingling")
    
    # Filter Tahun Berdasarkan Data yang Ada
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    
    start_year, end_year = st.slider(
        label='Rentang Tahun',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

# Filter Data Utama
main_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]

# --- Main Page Dashboard ---
st.header('Dashboard Kualitas Udara Stasiun Dingling :cloud:')

# 1. Tren Bulanan
st.subheader('Tren Bulanan PM2.5')
monthly_df = create_monthly_df(main_df)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(monthly_df["datetime"], monthly_df["PM2.5"], marker='o', linewidth=2, color="#3498db")
ax.set_title("Rata-rata Konsentrasi PM2.5 Bulanan", fontsize=20)
st.pyplot(fig)
st.write("Insight: Terlihat pola musiman di mana polusi melonjak tajam pada awal tahun.")

# 2. Layout Kolom (Tahunan & Harian)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Tahunan")
    yearly_df = create_yearly_df(main_df)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=yearly_df, x='year', y='PM2.5', hue='year', palette="viridis", ax=ax, legend=False)
    st.pyplot(fig)

with col2:
    st.subheader("Pola Harian (Jam)")
    hourly_df = create_hourly_df(main_df)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.lineplot(data=hourly_df, x='hour', y='PM2.5', marker='o', color="#e74c3c", ax=ax)
    st.pyplot(fig)

# 3. Analisis Lanjutan (Clustering)
st.subheader("Distribusi Kategori Kualitas Udara")
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
              palette='rocket', hue='AQI_Category', ax=ax, legend=False)
st.pyplot(fig)

st.caption('Naufal Daffa Abdu Al Hafidl')