import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# 1. Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    page_icon="🌬️",
    layout="wide"
)

# Set tema visual Seaborn
sns.set_theme(style="whitegrid")

# 2. Fungsi load data dengan caching
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

# --- SIDEBAR: Filter Dinamis ---
with st.sidebar:
    st.title("⚙️ Kontrol Panel")
    
    # Filter Rentang Waktu
    min_date = all_df["datetime"].min()
    max_date = all_df["datetime"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Filter Stasiun
    stasiun_list = all_df["station"].unique()
    stations = st.multiselect(
        "Pilih Lokasi Stasiun:",
        options=stasiun_list,
        default=stasiun_list
    )

# Proses filtering data
main_df = all_df[
    (all_df["datetime"] >= pd.to_datetime(start_date)) & 
    (all_df["datetime"] <= pd.to_datetime(end_date)) &
    (all_df["station"].isin(stations))
]

# --- MAIN PAGE: Header ---
st.title("🌬️ Air Quality Analysis Dashboard")
st.markdown(f"""
Selamat datang di dashboard analisis kualitas udara. Dashboard ini menyajikan data PM2.5 secara interaktif.
- **Nama:** Naufal Daffa Abdu Al Hafidl
- **Periode Data:** {start_date} s/d {end_date}
""")

st.divider()

# --- SECTION 1: Key Performance Indicators (KPI) ---
# Image of Key Performance Indicators (KPI) dashboard elements
st.subheader(" Statistik Utama (Terfilter)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Observasi", value=f"{main_df.shape[0]:,}")
with col2:
    avg_pm = main_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm:.2f} µg/m³")
with col3:
    max_pm = main_df['PM2.5'].max()
    st.metric("Konsentrasi Tertinggi", value=f"{max_pm:.1f} µg/m³")
with col4:
    st.metric("Jumlah Stasiun", value=main_df['station'].nunique())

st.divider()

# --- SECTION 2: Analisis Pertanyaan Bisnis dengan TABS ---
# Image of a tabbed interface in a web dashboard
tab1, tab2, tab3 = st.tabs([" Tren Bulanan", " Analisis Lokasi", " Pola Harian"])

# --- TAB 1: Tren Bulanan ---
with tab1:
    st.header("Bagaimana tren kualitas udara (PM2.5) berdasarkan waktu?")
    monthly_trend = main_df.groupby('month')['PM2.5'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=monthly_trend, x="month", y="PM2.5", 
        marker='o', linewidth=3, color='#3970F1', ax=ax
    )
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.set_title("Rata-rata Konsentrasi PM2.5 Per Bulan", fontsize=14)
    st.pyplot(fig)
    
    with st.expander("💡 Lihat Analisis"):
        st.write("""
        Grafik menunjukkan fluktuasi musiman yang jelas. Konsentrasi polutan mencapai puncaknya pada bulan-bulan dingin (Januari/Desember) 
        dan menurun secara drastis di pertengahan tahun (Mei-Agustus). Hal ini kemungkinan dipengaruhi oleh suhu udara dan aktivitas pembakaran pemanas.
        """)

# --- TAB 2: Analisis Lokasi ---
with tab2:
    st.header("Stasiun mana dengan polusi tertinggi dan terendah?")
    station_rank = main_df.groupby('station')['PM2.5'].mean().sort_values(ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=station_rank, x="PM2.5", y="station", 
        palette="Blues_r", ax=ax
    )
    ax.set_title("Peringkat Stasiun Berdasarkan Rata-rata PM2.5", fontsize=14)
    st.pyplot(fig)

    col_a, col_b = st.columns(2)
    col_a.success(f" **Stasiun Paling Bersih:** {station_rank['station'].iloc[-1]}")
    col_b.error(f" **Stasiun Paling Polusi:** {station_rank['station'].iloc[0]}")

# --- TAB 3: Pola Harian ---
with tab3:
    st.header("Kapan waktu paling berbahaya dalam sehari?")
    hourly_trend = main_df.groupby('hour')['PM2.5'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=hourly_trend, x="hour", y="PM2.5", 
        color='#E64545', linewidth=3, ax=ax
    )
    ax.fill_between(hourly_trend['hour'], hourly_trend['PM2.5'], color='#E64545', alpha=0.1)
    ax.set_xticks(range(0, 24))
    ax.set_title("Rata-rata Konsentrasi PM2.5 Per Jam", fontsize=14)
    st.pyplot(fig)

    st.warning(" **Insight:** Terdapat lonjakan polusi pada jam berangkat kerja (pagi) dan jam pulang kerja hingga malam hari. Pukul 12:00-15:00 adalah waktu dengan udara paling bersih.")

st.divider()
st.caption("Copyright (c) Naufal Daffa 2026 - Air Quality Project | Dicoding Submission")