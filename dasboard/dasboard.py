import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dingling Air Quality Dashboard",
    page_icon="☁️",
    layout="wide"
)

# Tema Visual
sns.set(style='whitegrid')
plt.rcParams['axes.facecolor'] = '#f9f9f9'

# Path Data
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "all_data.csv")

# --- Load Data ---
@st.cache_data
def load_data():
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    return None

df = load_data()

if df is None:
    st.error(f"Error: File 'all_data.csv' tidak ditemukan di folder {current_dir}")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.title("Filter Panel")
    
    # Filter Tahun
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.slider("Pilih Rentang Tahun", min_year, max_year, (min_year, max_year))
    
    st.markdown("---")
    st.markdown("**Analisis Oleh:**")
    st.write("Naufal Daffa Abdu Al Hafidl")
    st.caption("Proyek Analisis Data - Dicoding")

# Filter Data
main_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# --- Main Dashboard ---
st.title("☁️ Dingling Air Quality Dashboard")
st.markdown("Dashboard ini menyajikan analisis mendalam mengenai konsentrasi polutan PM2.5 di Stasiun Dingling.")

# Metrics Highlights
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    avg_pm = round(main_df['PM2.5'].mean(), 2)
    st.metric("Rata-rata PM2.5", f"{avg_pm} µg/m³")
with col_m2:
    max_pm = round(main_df['PM2.5'].max(), 2)
    st.metric("Puncak Polusi (Max)", f"{max_pm} µg/m³")
with col_m3:
    unhealthy_ratio = round((main_df['PM2.5'] > 55.4).mean() * 100, 1)
    st.metric("% Kategori Tidak Sehat", f"{unhealthy_ratio}%")

st.markdown("---")

# --- Visualisasi 1: Tren Waktu ---
st.subheader("1. Tren Kualitas Udara (PM2.5) Berdasarkan Waktu")
monthly_df = main_df.resample(rule='M', on='datetime').agg({"PM2.5": "mean"}).reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(monthly_df["datetime"], monthly_df["PM2.5"], marker='o', color='#2e86de', linewidth=2, markersize=5)
ax1.fill_between(monthly_df["datetime"], monthly_df["PM2.5"], color='#2e86de', alpha=0.1)
ax1.set_ylabel("Konsentrasi PM2.5")
st.pyplot(fig1)

with st.expander("💡 Klik untuk melihat Insight Tren Waktu"):
    st.write("- **Pola Musiman:** Terjadi lonjakan polusi signifikan di setiap akhir dan awal tahun (musim dingin).")
    st.write("- **Anomali Puncak:** Januari 2014 mencatatkan rekor polusi bulanan tertinggi selama periode observasi.")

# --- Visualisasi 2 & 3: Perbandingan Tahun & Jam ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("2. Rata-rata Tahunan")
    yearly_df = main_df.groupby('year')['PM2.5'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=yearly_df, x='year', y='PM2.5', palette="Blues_d", ax=ax2)
    st.pyplot(fig2)
    st.caption("Tahun 2016 tercatat sebagai tahun dengan kualitas udara terbaik.")

with col_right:
    st.subheader("3. Pola Konsentrasi Harian")
    hourly_df = main_df.groupby('hour')['PM2.5'].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.lineplot(data=hourly_df, x='hour', y='PM2.5', marker='o', color="#e74c3c", linewidth=2.5, ax=ax3)
    ax3.set_xticks(range(0, 24))
    st.pyplot(fig3)
    st.caption("Puncak polusi terjadi pada malam hari (18:00 - 21:00).")

# --- Visualisasi 4: Analisis Lanjutan (AQI Clustering) ---
st.markdown("---")
st.subheader("4. Analisis Lanjutan: Distribusi Kategori Kualitas Udara")

def categorize_aqi(val):
    if val <= 12: return 'Good'
    elif val <= 35.4: return 'Moderate'
    elif val <= 55.4: return 'Unhealthy for Sensitive Groups'
    elif val <= 150.4: return 'Unhealthy'
    else: return 'Very Unhealthy'

main_df['AQI_Category'] = main_df['PM2.5'].apply(categorize_aqi)
cat_order = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy']

fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.countplot(data=main_df, x='AQI_Category', order=cat_order, palette='viridis', ax=ax4)
plt.xticks(rotation=15)
st.pyplot(fig4)

with st.expander("💡 Klik untuk melihat Insight Analisis Lanjutan"):
    st.write("Meskipun Dingling berada di area pinggiran, frekuensi kategori **'Unhealthy'** mendominasi dataset, menunjukkan risiko kesehatan yang persisten.")

# --- Conclusion ---
st.markdown("---")
st.subheader("📌 Conclusion")
st.info("""
1. **Tren Waktu:** Polusi PM2.5 bersifat musiman dengan tingkat bahaya tertinggi di musim dingin.
2. **Performa Tahunan:** Terdapat fluktuasi yang dinamis, dengan titik terbersih dicapai pada tahun 2016.
3. **Pola Harian:** Akumulasi polutan meningkat drastis setelah matahari terbenam; masyarakat disarankan mengurangi aktivitas luar ruang di malam hari.
4. **Status AQI:** Secara keseluruhan, kategori 'Tidak Sehat' (Unhealthy) muncul paling sering, menegaskan perlunya kebijakan pengendalian emisi berkelanjutan.
""")

st.caption("Copyright © 2026 | Naufal Daffa - Proyek Analisis Data Air Quality")