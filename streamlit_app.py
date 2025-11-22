import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
from kagglehub import KaggleDatasetAdapter

st.set_page_config(page_title="E‑Commerce Event History Dashboard", 
                   page_icon="📊", layout="wide")

# Memuat dataset dari Kaggle
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "mkechinov/ecommerce-events-history-in-electronics-store",
    "events.csv",
)

# Konversi kolom waktu
df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
year = st.sidebar.selectbox("Pilih Tahun", options=['All'] + sorted(df['event_time'].dt.year.dropna().astype(int).astype(str).unique().tolist()))
month = st.sidebar.selectbox("Pilih Bulan", options=['All'] + sorted(df['event_time'].dt.month_name().dropna().unique().tolist()))
day = st.sidebar.selectbox("Pilih Hari", options=['All'] + sorted(df['event_time'].dt.day_name().dropna().unique().tolist()))
event_type = st.sidebar.multiselect("Pilih Tipe Event", options=['view', 'cart', 'purchase'], default=['view','cart','purchase'])

# Terapkan filter
df_filtered = df.copy()
if year != 'All':
    df_filtered = df_filtered[df_filtered['event_time'].dt.year == int(year)]
if month != 'All':
    df_filtered = df_filtered[df_filtered['event_time'].dt.month_name() == month]
if day != 'All':
    df_filtered = df_filtered[df_filtered['event_time'].dt.day_name() == day]
if event_type:
    df_filtered = df_filtered[df_filtered['event_type'].isin(event_type)]

# Hitung KPI
user_count = df_filtered['user_id'].nunique()
event_count = len(df_filtered)
avg_event_per_user = event_count / user_count if user_count else 0
# Proporsi cart & purchase dari total
prop_cart = df_filtered[df_filtered['event_type']=='cart'].shape[0] / event_count if event_count else 0
prop_purchase = df_filtered[df_filtered['event_type']=='purchase'].shape[0] / event_count if event_count else 0

# Header dan KPI cards
st.title("📊 eCommerce Event History Dashboard")
st.markdown(""" 
### Dashboard interaktif untuk menganalisis interaksi pengguna (view, cart, purchase) pada platform e-commerce.
Pilih filter di sidebar untuk menyesuaikan tampilan data dan grafik.
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{user_count:,}")
col2.metric("Total Events", f"{event_count:,}")
col3.metric("Avg Events/User", f"{avg_event_per_user:.2f}")
col4.metric("Cart % of Events", f"{prop_cart*100:.1f}%")
col5, col6 = st.columns([1,3])
col5.metric("Purchase % of Events", f"{prop_purchase*100:.1f}%")

# Pie Chart untuk Proporsi Event Type
st.subheader("Distribusi Tipe Event")
# Mengatasi masalah warna dan data yang hilang dengan fillna untuk kolom 'event_type'
df_filtered['event_type'] = df_filtered['event_type'].fillna('Unknown')

# Membuat pie chart dengan warna yang terkontrol
color_map = {'view': 'blue', 'cart': 'green', 'purchase': 'red', 'Unknown': 'gray'}
fig1 = px.pie(df_filtered, names='event_type', title="Proporsi view / cart / purchase", 
              color='event_type', color_discrete_map=color_map)
fig1.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font_color='white')
st.plotly_chart(fig1)
# --- Distribusi Event per Brand ---
st.subheader("Distribusi Event per Brand")

# Menghitung jumlah event per brand
brand_event_counts = df_filtered['brand'].value_counts().head(10).reset_index()
brand_event_counts.columns = ['Brand', 'Event Count']

# Membuat grafik bar untuk distribusi event per brand
fig_brand_event = px.bar(brand_event_counts, x='Event Count', y='Brand', orientation='h', title="Top 10 Brand berdasarkan Event",
                         color='Event Count', color_continuous_scale='Blues', labels={'Event Count': 'Jumlah Event'})
fig_brand_event.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font_color='white')
st.plotly_chart(fig_brand_event)

# --- Distribusi Brand berdasarkan Purchase ---
st.subheader("Distribusi Brand berdasarkan Purchase")

# Menghitung jumlah purchase per brand
brand_purchase_counts = df_filtered[df_filtered['event_type'] == 'purchase']['brand'].value_counts().head(10).reset_index()
brand_purchase_counts.columns = ['Brand', 'Purchase Count']

# Membuat grafik bar untuk distribusi purchase per brand
fig_brand_purchase = px.bar(brand_purchase_counts, x='Purchase Count', y='Brand', orientation='h', title="Top 10 Brand berdasarkan Purchase",
                            color='Purchase Count', color_continuous_scale='Greens', labels={'Purchase Count': 'Jumlah Purchase'})
fig_brand_purchase.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font_color='white')
st.plotly_chart(fig_brand_purchase)

# Event per Jam
st.subheader("Distribusi Event per Jam")

# Menambahkan kolom 'hour' untuk memisahkan data berdasarkan jam
df_filtered['hour'] = df_filtered['event_time'].dt.hour

# Menghitung jumlah event per jam
hour_counts = df_filtered.groupby('hour').size().reset_index(name='Event Count')

# Membuat label waktu yang lebih informatif untuk sumbu X (00:00 - 23:00)
hour_counts['hour_label'] = hour_counts['hour'].apply(lambda x: f"{x:02d}:00")

# Membuat grafik garis untuk distribusi event per jam dengan label waktu
fig4 = px.line(hour_counts, x='hour_label', y='Event Count', title="Event per Jam", markers=True)

# Mengatur tema dan desain untuk grafik
fig4.update_layout(
    plot_bgcolor='#0E1117',  # Latar belakang grafik
    paper_bgcolor='#0E1117',  # Latar belakang keseluruhan
    font_color='white',  # Warna font putih
    xaxis_title="Waktu (Jam)",  # Label untuk sumbu X
    yaxis_title="Jumlah Event",  # Label untuk sumbu Y
    xaxis=dict(showgrid=True),  # Menampilkan grid pada sumbu X
    yaxis=dict(showgrid=True),  # Menampilkan grid pada sumbu Y
    xaxis_tickangle=45  # Memiringkan label pada sumbu X agar lebih terbaca
)

# Menampilkan grafik interaktif di Streamlit
st.plotly_chart(fig4)


# Event per Hari dalam Seminggu
st.subheader("Distribusi Event per Hari dalam Seminggu")

# Pastikan event_time memiliki nilai yang valid dan dapat dikonversi ke nama hari
df_filtered['day_name'] = df_filtered['event_time'].dt.day_name()

# Memeriksa apakah ada data yang kosong pada kolom day_name
if df_filtered['day_name'].isnull().sum() > 0:
    st.write("Beberapa data 'event_time' memiliki nilai yang tidak valid atau kosong.")

# Mengelompokkan data berdasarkan hari dalam minggu dan menghitung jumlah event
day_counts = df_filtered.groupby('day_name').size().reset_index(name='Event Count')

# Urutkan data agar hari-hari dimulai dari Senin dan berakhir pada Minggu
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_counts = day_counts.set_index('day_name').reindex(day_order).reset_index()

# Cek apakah ada data setelah reindexing
if day_counts.isnull().sum().sum() > 0:
    st.write("Beberapa hari tidak memiliki data event. Periksa data Anda.")

# Membuat grafik garis untuk distribusi event per hari
fig5 = px.line(day_counts, x='day_name', y='Event Count', title="Event per Hari dalam Seminggu", markers=True)
fig5.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font_color='white')
st.plotly_chart(fig5)

# Event per Bulan
st.subheader("Distribusi Event per Bulan")

# Membuat kolom yang berisi bulan dan tahun
df_filtered['month_year'] = df_filtered['event_time'].dt.to_period('M').astype(str)

# Mengelompokkan data berdasarkan bulan dan tahun (month_year)
month_counts = df_filtered.groupby('month_year').size().reset_index(name='Event Count')

# Membuat grafik garis untuk distribusi event per bulan
fig6 = px.line(month_counts, x='month_year', y='Event Count', title="Event per Bulan", markers=True)

# Mengatur tema dan desain
fig6.update_layout(
    plot_bgcolor='#0E1117',  # Latar belakang grafik
    paper_bgcolor='#0E1117',  # Latar belakang keseluruhan
    font_color='white',  # Warna font putih
    xaxis_title="Month and Year",  # Label untuk sumbu X (Bulan dan Tahun)
    yaxis_title="Event Count",  # Label untuk sumbu Y (Jumlah Event)
    xaxis=dict(showgrid=True),  # Menampilkan grid pada sumbu X
    yaxis=dict(showgrid=True)  # Menampilkan grid pada sumbu Y
)

# Menampilkan grafik interaktif di Streamlit
st.plotly_chart(fig6)

# Tampilkan preview data
st.subheader("Preview Data")
st.dataframe(df_filtered)

st.markdown("---")
st.markdown("© 2025 Dashboard oleh Andrianus Alvien")
