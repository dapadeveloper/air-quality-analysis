import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================================
# KONFIGURASI HALAMAN (WAJIB HANYA 1 KALI)
# =====================================================
st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    layout="wide"
)

# =====================================================
# JUDUL & DESKRIPSI
# =====================================================
st.title("☁️ Air Quality Analysis Dashboard")
st.write(
    "Dashboard ini menampilkan hasil analisis kualitas udara "
    "berdasarkan Dataset Air Quality pada Stasiun **Huairou**."
)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "all_data.csv")

    df = pd.read_csv(data_path)

    # Feature Engineering: membuat kolom date
    if {"year", "month", "day"}.issubset(df.columns):
        df["date"] = pd.to_datetime(df[["year", "month", "day"]])

    return df


try:
    df = load_data()
except Exception as e:
    st.error("❌ Gagal memuat data. Pastikan file `all_data.csv` berada di folder `dasboard`.")
    st.error(f"Detail error: {e}")
    st.stop()

# =====================================================
# SIDEBAR - FILTER DATA
# =====================================================
with st.sidebar:
    st.header("🔎 Filter Waktu")

    start_date = st.date_input(
        "Tanggal Mulai",
        df["date"].min().date()
    )

    end_date = st.date_input(
        "Tanggal Akhir",
        df["date"].max().date()
    )

# Filter dataframe berdasarkan tanggal
filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

# =====================================================
# RINGKASAN STATISTIK
# =====================================================
st.subheader("📊 Ringkasan Statistik Polutan")

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Rata-rata PM2.5",
    value=f"{filtered_df['PM2.5'].mean():.2f}"
)

col2.metric(
    label="Rata-rata PM10",
    value=f"{filtered_df['PM10'].mean():.2f}"
)

col3.metric(
    label="Rata-rata NO2",
    value=f"{filtered_df['NO2'].mean():.2f}"
)

st.markdown("---")

# =====================================================
# PERTANYAAN 1
# Tren Polutan dari Waktu ke Waktu
# =====================================================
st.subheader("1️⃣ Bagaimana tren konsentrasi polutan dari waktu ke waktu?")

polutan_list = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
selected_polutan = st.selectbox("Pilih jenis polutan:", polutan_list)

monthly_df = (
    filtered_df
    .set_index("date")
    .resample("M")
    .mean(numeric_only=True)
)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    monthly_df.index,
    monthly_df[selected_polutan],
    linewidth=2
)
ax.set_title(f"Rata-rata Bulanan {selected_polutan}")
ax.set_xlabel("Tahun")
ax.set_ylabel("Konsentrasi")
ax.grid(alpha=0.4)

st.pyplot(fig)

st.write(
    f"**Insight:** Grafik menunjukkan bahwa konsentrasi **{selected_polutan}** "
    "mengalami fluktuasi dari waktu ke waktu dengan pola tertentu. "
    "Hal ini mengindikasikan adanya pengaruh faktor musiman serta aktivitas manusia "
    "terhadap kualitas udara di Stasiun Huairou."
)

st.markdown("---")

# =====================================================
# PERTANYAAN 2
# Pengaruh Faktor Cuaca terhadap PM2.5
# =====================================================
st.subheader("2️⃣ Bagaimana pengaruh faktor cuaca terhadap konsentrasi PM2.5?")

left_col, right_col = st.columns(2)

with left_col:
    weather_var = st.radio(
        "Pilih variabel cuaca:",
        ["TEMP", "DEWP"],
        horizontal=True
    )

    sample_df = filtered_df.sample(
        n=min(1000, len(filtered_df)),
        random_state=42
    )

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.regplot(
        x=weather_var,
        y="PM2.5",
        data=sample_df,
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red"}
    )
    ax2.set_title(f"Korelasi {weather_var} terhadap PM2.5")

    st.pyplot(fig2)

with right_col:
    corr_value = filtered_df[weather_var].corr(filtered_df["PM2.5"])

    st.metric(
        label=f"Koefisien Korelasi {weather_var} vs PM2.5",
        value=f"{corr_value:.3f}"
    )

    if corr_value > 0:
        st.write(
            f"**Insight:** Terdapat korelasi **positif** antara {weather_var} dan PM2.5. "
            "Artinya, peningkatan nilai variabel cuaca ini cenderung diikuti "
            "oleh peningkatan konsentrasi PM2.5."
        )
    else:
        st.write(
            f"**Insight:** Terdapat korelasi **negatif** antara {weather_var} dan PM2.5. "
            "Artinya, peningkatan nilai variabel cuaca ini cenderung diikuti "
            "oleh penurunan konsentrasi PM2.5."
        )

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("📘 Proyek Analisis Data Air Quality | Dashboard Streamlit")
