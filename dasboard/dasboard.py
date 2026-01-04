import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

st.title("☁️ Air Quality Analysis Dashboard")
st.write("Analisis Kualitas Udara – Dataset Air Quality (Stasiun Huairou)")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    layout="wide"
)

# ==============================
# LOAD DATA 
# ==============================
@st.cache_data
def load_data():
    # Ambil path folder tempat dasboard.py berada
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Gabungkan dengan nama file CSV
    DATA_PATH = os.path.join(BASE_DIR, "all_data.csv")

    df = pd.read_csv(DATA_PATH)

    # Feature engineering kolom date
    if {'year', 'month', 'day'}.issubset(df.columns):
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    return df


try:
    df = load_data()
except Exception as e:
    st.error("Gagal memuat data. Pastikan file 'all_data.csv' berada di folder 'dasboard'.")
    st.error(f"Detail error: {e}")
    st.stop()


# ===============================
# SIDEBAR FILTER
# ===============================
with st.sidebar:
    st.header("🔎 Filter Data")

    start_date = st.date_input(
        "Tanggal Mulai",
        df['date'].min().date()
    )

    end_date = st.date_input(
        "Tanggal Akhir",
        df['date'].max().date()
    )

# Filter data berdasarkan tanggal
main_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
]

# ===============================
# RINGKASAN METRIK
# ===============================
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)

col1.metric("Rata-rata PM2.5", f"{main_df['PM2.5'].mean():.2f}")
col2.metric("Rata-rata PM10", f"{main_df['PM10'].mean():.2f}")
col3.metric("Rata-rata NO2", f"{main_df['NO2'].mean():.2f}")

st.markdown("---")

# ===============================
# PERTANYAAN 1
# Tren Polutan dari Waktu ke Waktu
# ===============================
st.subheader("1️⃣ Tren Konsentrasi Polutan dari Waktu ke Waktu")

polutan_list = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
selected_polutan = st.selectbox(
    "Pilih Parameter Polutan:",
    polutan_list
)

monthly_df = (
    main_df
    .set_index('date')
    .resample('M')
    .mean(numeric_only=True)
)

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(
    monthly_df.index,
    monthly_df[selected_polutan],
    linewidth=2
)
ax1.set_title(f"Rata-rata Bulanan {selected_polutan}")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Konsentrasi")
ax1.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig1)

st.write(
    f"Grafik menunjukkan perubahan rata-rata bulanan **{selected_polutan}** "
    "selama periode pengamatan."
)

st.markdown("---")

# ===============================
# PERTANYAAN 2
# Faktor Cuaca terhadap PM2.5
# ===============================
st.subheader("2️⃣ Analisis Faktor Cuaca terhadap PM2.5")

col1, col2 = st.columns(2)

with col1:
    var_x = st.radio(
        "Pilih Faktor Cuaca:",
        ["TEMP", "DEWP"],
        horizontal=True
    )

    sample_df = main_df.sample(
        n=min(1000, len(main_df)),
        random_state=42
    )

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.regplot(
        x=var_x,
        y="PM2.5",
        data=sample_df,
        ax=ax2,
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red"}
    )
    ax2.set_title(f"Korelasi {var_x} terhadap PM2.5")

    st.pyplot(fig2)

with col2:
    st.write("### Insight")
    correlation = main_df[var_x].corr(main_df['PM2.5'])

    st.metric(
        label=f"Nilai Korelasi {var_x} vs PM2.5",
        value=f"{correlation:.3f}"
    )

    if correlation > 0:
        st.write(
            f"Terdapat **korelasi positif** antara {var_x} dan PM2.5, "
            "di mana peningkatan nilai variabel cuaca cenderung diikuti "
            "peningkatan konsentrasi PM2.5."
        )
    else:
        st.write(
            f"Terdapat **korelasi negatif** antara {var_x} dan PM2.5, "
            "di mana peningkatan nilai variabel cuaca cenderung diikuti "
            "penurunan konsentrasi PM2.5."
        )

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("Air Quality Project Submission | Dashboard Streamlit")