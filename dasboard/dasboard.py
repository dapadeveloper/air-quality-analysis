import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# 1. LOAD DATA 
# Menyesuaikan dengan path di gambar: dasboard/all_data.csv
@st.cache_data
def load_data():
    # Menggunakan path relatif sesuai struktur folder kamu
    df = pd.read_csv("dasboard/all_data.csv")
    
    # Memastikan kolom date dalam format datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        # Jika belum ada kolom date, kita buat dari year, month, day
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file berada di: dasboard/all_data.csv. Error: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Filter Dataset")
    
    # Filter Stasiun
    stasiun = st.selectbox(
        label="Pilih Stasiun",
        options=["Semua Stasiun"] + list(df['station'].unique())
    )

# Filter Data berdasarkan sidebar
main_df = df if stasiun == "Semua Stasiun" else df[df['station'] == stasiun]

# --- MAIN PAGE ---
st.header('Air Quality Analysis Dashboard ☁️')

# Pertanyaan 1: Tren Polutan
st.subheader('1. Tren Konsentrasi Polutan dari Waktu ke Waktu')

# Pilihan polutan untuk tren
polutan_list = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
selected_polutan = st.selectbox("Pilih Parameter Polutan:", polutan_list)

# Plotting Tren
fig, ax = plt.subplots(figsize=(12, 5))
# Resample bulanan agar grafik lebih halus dan mudah dibaca
monthly_df = main_df.set_index('date').resample('M').mean(numeric_only=True)

ax.plot(monthly_df.index, monthly_df[selected_polutan], color='#2471A3', linewidth=2)
ax.set_title(f'Rata-rata Bulanan {selected_polutan}', fontsize=16)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Konsentrasi', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)

st.pyplot(fig)

st.write(f"Grafik di atas menunjukkan fluktuasi rata-rata {selected_polutan} di stasiun {stasiun}.")

st.markdown("---")

# Pertanyaan 2: Hubungan Suhu & Kelembaban vs PM2.5
st.subheader('2. Analisis Faktor Cuaca terhadap PM2.5')

col1, col2 = st.columns(2)

with col1:
    var_x = st.radio("Pilih Faktor Cuaca:", ["TEMP", "DEWP"], horizontal=True)
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    # Mengambil sampel 1000 data saja agar dashboard tetap ringan saat plotting
    sample_df = main_df.sample(n=min(1000, len(main_df)))
    
    sns.regplot(x=var_x, y="PM2.5", data=sample_df, ax=ax2, 
                scatter_kws={'alpha':0.4, 'color':'#2ECC71'}, 
                line_kws={'color':'red'})
    
    ax2.set_title(f'Korelasi {var_x} vs PM2.5')
    st.pyplot(fig2)

with col2:
    st.write("### Insight")
    correlation = main_df[var_x].corr(main_df['PM2.5'])
    st.metric(label=f"Nilai Korelasi {var_x}", value=f"{correlation:.3f}")
    
    if correlation > 0:
        st.write(f"Terdapat korelasi **positif** antara {var_x} dan PM2.5.")
    else:
        st.write(f"Terdapat korelasi **negatif** antara {var_x} dan PM2.5.")

st.caption('Copyright © 2024 - Air Quality Project Submission')