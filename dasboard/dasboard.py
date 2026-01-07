import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Setup style seaborn
sns.set(style='dark')

# Helper function untuk menyiapkan berbagai dataframe
def create_yearly_avg_df(df):
    yearly_avg_df = df.groupby('year')['PM2.5'].mean().reset_index()
    return yearly_avg_df

def create_station_avg_df(df):
    station_avg_df = df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
    return station_avg_df

def create_hourly_avg_df(df):
    hourly_avg_df = df.groupby("hour")["PM2.5"].mean().reset_index()
    return hourly_avg_df

# Load data (Pastikan file all_data.csv ada di folder yang sama)
all_df = pd.read_csv("all_data.csv")

# Filter Sidebar
st.sidebar.header("Filter Data")
station_option = st.sidebar.multiselect(
    "Pilih Stasiun:",
    options=all_df["station"].unique(),
    default=all_df["station"].unique()
)

# Filter dataframe berdasarkan sidebar
main_df = all_df[all_df["station"].isin(station_option)]

# Judul Dashboard
st.title("Proyek Analisis Data: Air Quality Dashboard ")
st.markdown(f"Nama: **Naufal Daffa Abdu Al Hafidl** | Email: **fahmifalah081120@gmail.com**")

# Layout Column untuk Metric Utama
col1, col2 = st.columns(2)
with col1:
    avg_pm25 = main_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f} µg/m³")
with col2:
    highest_station = main_df.groupby("station")["PM2.5"].mean().idxmax()
    st.metric("Stasiun Polusi Tertinggi", value=highest_station)

st.divider()

# --- Pertanyaan 1: Tren Tahunan ---
st.subheader("1. Tren Kualitas Udara (PM2.5) per Tahun")
yearly_df = create_yearly_avg_df(main_df)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(yearly_df["year"], yearly_df["PM2.5"], marker='o', linewidth=2, color="#3975d4")
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig)

# --- Pertanyaan 2: Perbandingan Stasiun ---
st.subheader("2. Perbandingan Polusi Antar Stasiun")
station_df = create_station_avg_df(main_df)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#D32F2F" if (i == 0) else "#2E7D32" if (i == len(station_df)-1) else "#D3D3D3" for i in range(len(station_df))]
sns.barplot(x="PM2.5", y="station", data=station_df, palette=colors, ax=ax)
ax.set_title("Stasiun dengan Polusi Tertinggi (Merah) & Terendah (Hijau)")
st.pyplot(fig)

# --- Pertanyaan 3: Pola Harian ---
st.subheader("3. Pola Konsentrasi PM2.5 Berdasarkan Jam")
hourly_df = create_hourly_avg_df(main_df)
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_df, x="hour", y="PM2.5", marker='o', color="#E67E22", ax=ax)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig)

# --- Kesimpulan ---
with st.expander("Lihat Kesimpulan dan Analisis Lanjutan"):
    st.write("""
    - **Tren**: Kualitas udara memburuk di musim dingin dan membaik di pertengahan tahun.
    - **Lokasi**: Stasiun **Dongsi** tertinggi dan **Dingling** terendah.
    - **Pola Harian**: Konsentrasi polutan tertinggi pada malam hari dan menurun di siang hari (12:00-15:00).
    - **Analisis Lanjutan**: Meskipun ada stasiun yang bersih, kategori 'Unhealthy' masih mendominasi jam pengamatan secara keseluruhan.
    """)

st.caption('Copyright (c) Naufal Daffa 2026')