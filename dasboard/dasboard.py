import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Setup style seaborn
sns.set(style='dark')

# --- Helper functions ---
def create_yearly_avg_df(df):
    return df.groupby('year')['PM2.5'].mean().reset_index()

def create_station_avg_df(df):
    return df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()

def create_hourly_avg_df(df):
    return df.groupby("hour")["PM2.5"].mean().reset_index()

# --- Load Data dengan Path Dinamis ---
# Kode ini memastikan streamlit mencari file di folder yang sama dengan skrip ini
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "all_data.csv")

@st.cache_data # Menambahkan cache agar loading lebih cepat
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # Mencoba mencari di root jika tidak ada di folder dashboard
        return pd.read_csv("all_data.csv")

try:
    all_df = load_data(file_path)

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
    st.title("Proyek Analisis Data: Air Quality Dashboard 🌬️")
    st.markdown(f"Nama: **Naufal Daffa Abdu Al Hafidl** | Email: **fahmifalah081120@gmail.com**")

    # Layout Column untuk Metric Utama
    col1, col2 = st.columns(2)
    with col1:
        avg_pm25 = main_df['PM2.5'].mean()
        st.metric("Rata-rata PM2.5 Global", value=f"{avg_pm25:.2f} µg/m³")
    with col2:
        if not main_df.empty:
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
    # Warna highlight
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
        - **Tren**: Kualitas udara memburuk di musim dingin dan membaik di pertengahan tahun. Hal ini dipengaruhi faktor musiman dan aktivitas pemanas ruangan.
        - **Lokasi**: Berdasarkan dataset, **Stasiun Dongsi** mencatat rata-rata tertinggi dan **Stasiun Dingling** mencatat rata-rata terendah.
        - **Pola Harian**: Konsentrasi polutan memuncak pada malam hingga pagi hari dan menurun signifikan di siang hari (12:00-15:00).
        - **Analisis Lanjutan**: Meskipun ada stasiun yang relatif bersih, frekuensi kategori 'Unhealthy' tetap tinggi secara keseluruhan, menunjukkan perlunya kesadaran penggunaan masker di Beijing.
        """)

except FileNotFoundError:
    st.error("Error: File 'all_data.csv' tidak ditemukan. Pastikan file tersebut berada di folder yang sama dengan dashboard.py.")

st.caption('Copyright (c) Naufal Daffa 2026')