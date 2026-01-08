import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi halaman
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Fungsi load data dengan penanganan path (menghindari FileNotFoundError)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "all_data.csv")
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

# Memanggil data
try:
    all_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Filter Analisis")
    
    # Filter Stasiun
    stations = st.multiselect(
        "Pilih Stasiun:",
        options=all_df["station"].unique(),
        default=all_df["station"].unique()
    )

# Filter data berdasarkan pilihan sidebar
main_df = all_df[all_df["station"].isin(stations)]

# --- MAIN PAGE ---
st.title("Air Quality Analysis Dashboard ")
st.markdown(f"**Nama:** {all_df.columns.get_loc if 'Nama' in locals() else 'Naufal Daffa Abdu Al Hafidl'}")

# Menampilkan Ringkasan Data
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Observasi", value=main_df.shape[0])
with col2:
    st.metric("Rata-rata PM2.5", value=round(main_df['PM2.5'].mean(), 2))
with col3:
    st.metric("Jumlah Stasiun", value=main_df['station'].nunique())

st.divider()

# --- URUTAN SESUAI PERTANYAAN BISNIS DI NOTEBOOK ---

# 1. Tren PM2.5 Berdasarkan Waktu (Bulanan)
st.header("1. Tren Kualitas Udara (PM2.5) Berdasarkan Waktu")
monthly_trend = main_df.groupby('month')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_trend.index, monthly_trend.values, marker='o', linewidth=2, color='#3970F1')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

st.info("💡 **Insight:** Konsentrasi PM2.5 cenderung meningkat pada bulan-bulan dingin (Januari & Desember) dan menurun di pertengahan tahun.")

# 2. Lokasi/Stasiun Tertinggi & Terendah
st.header("2. Perbandingan Polusi PM2.5 Antar Stasiun")
station_rank = main_df.groupby('station')['PM2.5'].mean().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 6))
# Memberikan warna highlight pada yang tertinggi
colors = ["#D3D3D3"] * (len(station_rank) - 1) + ["#72BCD4"] 
station_rank.plot(kind='barh', color=colors, ax=ax)
ax.set_xlabel("Rata-rata Konsentrasi PM2.5 (µg/m³)", fontsize=12)
ax.set_ylabel("Nama Stasiun", fontsize=12)
st.pyplot(fig)

st.info("💡 **Insight:** Stasiun tertentu (seperti Dongsi/Guanyuan) menunjukkan tingkat polusi yang lebih kritis dibandingkan stasiun pinggiran seperti Dingling.")

# 3. Pola Konsentrasi Harian
st.header("3. Pola Konsentrasi PM2.5 Berdasarkan Waktu Harian")
hourly_trend = main_df.groupby('hour')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_trend.index, hourly_trend.values, color='#E64545', linewidth=2)
ax.fill_between(hourly_trend.index, hourly_trend.values, color='#E64545', alpha=0.1)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam (24 Jam)", fontsize=12)
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)", fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.info("💡 **Insight:** Terdapat pola bimodal (dua puncak) yang terjadi pada pagi hari dan malam hari, berkaitan dengan jam sibuk kendaraan.")

st.divider()
st.caption("Copyright (c) Naufal Daffa 2026 - Air Quality Project")