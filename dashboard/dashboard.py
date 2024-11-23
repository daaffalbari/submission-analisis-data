import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

# Fungsi untuk memuat data
@st.cache_resource
def load_data():
    day_df = pd.read_csv('dashboard/day_clean.csv')  
    hour_df = pd.read_csv('dashboard/hour_clean.csv')
    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Bike Sharing")
st.markdown("""
Dashboard ini memberikan wawasan tentang bagaimana penggunaan layanan *bike sharing* dipengaruhi oleh musim, cuaca, dan pola waktu tertentu (tahun, bulan, dan jam).
""")

# Sidebar untuk filter interaktif
st.sidebar.header("Pengaturan Filter")
selected_year = st.sidebar.multiselect(
    "Pilih Tahun", 
    options=day_df['yr'].unique(), 
    default=day_df['yr'].unique()
)

# Filter data berdasarkan tahun
day_df_filtered = day_df[day_df['yr'].isin(selected_year)]

# Bagaimana musim memengaruhi penggunaan layanan bike sharing
st.subheader("Jumlah Pengguna Berdasarkan Musim dan Tahun")
seasonal_data = day_df_filtered.groupby(['season', 'yr']).agg({'cnt': 'sum'}).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(
    data=seasonal_data,
    x='season',
    y='cnt',
    hue='yr',
    palette='Set2'
)
plt.title('Jumlah Pengguna Sepeda Berdasarkan Musim (2011 vs 2012)')
plt.xlabel('Musim')
plt.ylabel('Jumlah Pengguna')
plt.legend(title='Tahun')
st.pyplot(plt)

st.markdown("""
**Insight**:
1. **Peningkatan di Musim Gugur (Fall) dan Musim Panas (Summer)**:
   - Kedua musim ini menunjukkan jumlah pengguna yang paling tinggi, terutama pada tahun 2012. Hal ini menunjukkan bahwa cuaca di musim ini mungkin kondusif untuk bersepeda.
2. **Musim Semi (Spring) Paling Rendah**:
   - Penggunaan sepeda paling rendah di musim semi pada tahun 2011. Ini bisa jadi akibat kondisi cuaca yang kurang mendukung untuk bersepeda atau awal tahun yang lebih dingin.
""")

# Bagaimana cuaca memengaruhi penggunaan layanan bike sharing
st.subheader("Jumlah Pengguna Berdasarkan Cuaca")
weather_plot = day_df.groupby(by='weathersit').agg({'cnt': 'mean'}).reset_index()

plt.figure(figsize=(8, 4))
sns.barplot(
    data=weather_plot,
    x='weathersit',
    y='cnt',
    palette='Blues'
)
plt.title('Jumlah Pengguna Berdasarkan Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)

st.markdown("""
**Insight**: 
- Jumlah penggunaan layanan *bike sharing* paling tinggi terjadi pada cuaca yang cerah. 
- Hal ini menunjukkan bahwa cuaca cerah lebih disukai oleh pengguna layanan *bike sharing* dibandingkan kondisi cuaca lainnya.
""")

# Pola penggunaan berdasarkan tahun
st.subheader("Pola Penggunaan Berdasarkan Tahun")
plot_year = day_df.groupby(by='yr').agg({'cnt': 'mean'}).reset_index()

plt.figure(figsize=(5, 4))
sns.barplot(data=plot_year, x='yr', y='cnt', palette='viridis')
plt.title('Total Pengguna Sepeda per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Pengguna Sepeda')
st.pyplot(plt)

# Pola penggunaan berdasarkan bulan
st.subheader("Pola Penggunaan Berdasarkan Bulan")
day_df['cnt'] = pd.to_numeric(day_df['cnt'], errors='coerce')
day_df['mnth'] = pd.to_numeric(day_df['mnth'], errors='coerce')

monthly_data = day_df.groupby(by='mnth').agg({'cnt': 'sum'}).reset_index()
monthly_data['mnth_name'] = monthly_data['mnth'].apply(lambda x: calendar.month_name[x])

norm = plt.Normalize(monthly_data['cnt'].min(), monthly_data['cnt'].max())
colors = sns.color_palette('coolwarm', as_cmap=True)(norm(monthly_data['cnt']))

plt.figure(figsize=(12, 4))
sns.barplot(
    data=monthly_data.sort_values('mnth', ascending=True),
    x='mnth_name',
    y='cnt',
    palette=colors
)
plt.title('Jumlah Pengguna Sepeda Per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)

st.markdown("""
**Insight**: 
- **Peningkatan di Tengah Tahun**:
  - Jumlah peminjaman sepeda meningkat mulai sekitar bulan ke-4 hingga mencapai puncaknya pada bulan ke-6, ke-7, ke-8, dan ke-9. 
  - Hal ini menunjukkan bahwa musim panas dan musim liburan mendukung aktivitas bersepeda.
""")

# Pola penggunaan berdasarkan jam
st.subheader("Pola Penggunaan Berdasarkan Jam")
hour_df['cnt'] = pd.to_numeric(hour_df['cnt'], errors='coerce')
hour_df['hr'] = pd.to_numeric(hour_df['hr'], errors='coerce')

plt.figure(figsize=(8, 4))
sns.barplot(
    data=hour_df.sort_values('hr', ascending=False),
    x='hr',
    y='cnt',
    palette='coolwarm'
)
plt.title('Jumlah Pengguna Sepeda Per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)

st.markdown("""
**Insight**: 
- Pola penggunaan layanan *bike sharing* menunjukkan bahwa jam sibuk pagi dan sore hari (misalnya jam 7-9 pagi dan 5-7 sore) cenderung memiliki jumlah pengguna lebih tinggi. 
- Ini mengindikasikan banyak pengguna memanfaatkan layanan untuk perjalanan kerja atau sekolah.
""")

# Footer
st.markdown("Dashboard dibuat dengan ❤️ menggunakan Streamlit dan Matplotlib.")
