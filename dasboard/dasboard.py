import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load data yang sudah bersih
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

all_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Filter Data")
    
    # Filter Stasiun
    stations = st.multiselect(
        "Pilih Stasiun:",
        options=all_df["station"].unique(),
        default=all_df["station"].unique()
    )

# Filter data berdasarkan pilihan sidebar
main_df = all_df[all_df["station"].isin(stations)]

# --- MAIN PAGE ---
st.title("Air Quality Analysis Dashboard 🌬️")
st.markdown("Dashboard ini menyajikan hasil analisis kualitas udara (PM2.5) berdasarkan pertanyaan bisnis.")

# --- Pertanyaan 1: Tren Bulanan ---
st.header("1. Tren Kualitas Udara (PM2.5) Bulanan")
monthly_trend = main_df.groupby('month')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_trend.index, monthly_trend.values, marker='o', linewidth=2, color='#3970F1')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata PM2.5")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

with st.expander("Lihat Insight Tren Bulanan"):
    st.write("""
    Kualitas udara memburuk secara signifikan pada bulan **Januari, Februari, dan Desember**. 
    Hal ini menunjukkan pola musiman di mana polusi jauh lebih tinggi selama musim dingin.
    """)

# --- Pertanyaan 2: Perbandingan Stasiun ---
st.header("2. Tingkat Polusi Tertinggi & Terendah per Stasiun")
station_rank = main_df.groupby('station')['PM2.5'].mean().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#D3D3D3"] * (len(station_rank) - 1) + ["#72BCD4"] # Highlight tertinggi
station_rank.plot(kind='barh', color=colors, ax=ax)
ax.set_xlabel("Rata-rata PM2.5")
ax.set_ylabel("Stasiun")
st.pyplot(fig)

with st.expander("Lihat Insight Perbandingan Stasiun"):
    st.write("""
    Stasiun dengan rata-rata polusi tertinggi teridentifikasi di wilayah pusat kota, 
    sedangkan stasiun seperti **Dingling** secara konsisten menunjukkan tingkat polusi terendah.
    """)

# --- Pertanyaan 3: Pola Harian ---
st.header("3. Pola Konsentrasi Polutan Harian (Jam)")
hourly_trend = main_df.groupby('hour')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_trend.index, hourly_trend.values, color='#E64545', linewidth=2)
ax.fill_between(hourly_trend.index, hourly_trend.values, color='#E64545', alpha=0.1)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig)

with st.expander("Lihat Insight Pola Harian"):
    st.write("""
    Terdapat siklus dua puncak (pagi dan malam hari) yang berkorelasi dengan jam sibuk 
    aktivitas transportasi manusia.
    """)

st.caption('Copyright (c) Naufal Daffa 2026')