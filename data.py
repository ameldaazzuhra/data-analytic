import streamlit as st
import pandas as pd

# Load dataset
file_path = 'Dataset_APBN_2023.csv'  # Sesuaikan dengan lokasi file
data = pd.read_csv(file_path)

# Pastikan nama kolom sesuai
data.columns = data.columns.str.strip()  # Menghapus spasi ekstra pada nama kolom

# Title
st.title("Dashboard Pendidikan Indonesia")

# Membuat Tabs
tabs = st.tabs(["Analisis", "Ringkasan"])

# Tab Analisis
with tabs[0]:
    st.header("Analisis Data")

    # Sidebar Widgets
    st.sidebar.title("Filter Data")
    level = st.sidebar.radio("Pilih tingkat pendidikan:", ['SD', 'SMP', 'SMA', 'SMK'])
    provinces = st.sidebar.multiselect("Pilih provinsi:", data['PROVINSI'].unique())

    # Tanggal Input di Sidebar
    st.sidebar.title("Pilih Tanggal")
    selected_date = st.sidebar.date_input("Pilih tanggal data:", value=pd.Timestamp.today())

    # Filter data berdasarkan provinsi yang dipilih
    filtered_data = data[data['PROVINSI'].isin(provinces)]

    # Display data
    st.subheader(f"Data {level} di Provinsi: {', '.join(provinces)}")
    st.write(filtered_data)

    # Chart Dropdown (Pilih jenis chart yang akan ditampilkan)
    chart_type = st.selectbox("Pilih jenis chart:", ['Dropout', 'Jumlah Kuota Murid', 'Jumlah Murid'])

    # Visualisasi Berdasarkan Pilihan
    if chart_type == 'Dropout':
        st.subheader(f"Visualisasi Dropout {level}")
        dropout_column = f'Dropout {level}'
        if dropout_column in data.columns:
            st.bar_chart(filtered_data.set_index('PROVINSI')[dropout_column])
        else:
            st.write("Data dropout tidak tersedia di dataset.")

    elif chart_type == 'Jumlah Kuota Murid':
        st.subheader(f"Visualisasi Jumlah Kuota Murid {level}")
        kuota_column = f'Jumlah Kuota Murid {level}'
        if kuota_column in data.columns:
            st.bar_chart(filtered_data.set_index('PROVINSI')[kuota_column])
        else:
            st.write("Data kuota murid tidak tersedia di dataset.")

    elif chart_type == 'Jumlah Murid':
        st.subheader(f"Visualisasi Jumlah Murid {level}")
        murid_column = f'Jumlah Murid {level}'
        if murid_column in data.columns:
            st.bar_chart(filtered_data.set_index('PROVINSI')[murid_column])
        else:
            st.write("Data jumlah murid tidak tersedia di dataset.")

# Tab Ringkasan
with tabs[1]:
    st.header("Ringkasan Data")

    # Membuat 3 Kolom untuk Ringkasan
    col1, col2, col3 = st.columns(3)

    # Menghitung Total Jumlah Murid
    with col1:
        total_students = data[[col for col in data.columns if 'Jumlah Murid' in col]].sum().sum()
        st.metric("Jumlah Total Murid", f"{total_students:,}")

    # Menghitung Total Jumlah Pagu
    with col2:
        total_budget = data[[col for col in data.columns if 'PAGU' in col]].sum().sum()
        st.metric("Jumlah Total Pagu", f"{total_budget:,}")

    # Menghitung Total Jumlah Sekolah
    with col3:
        total_schools = data[[col for col in data.columns if 'Jumlah Sekolah' in col]].sum().sum()
        st.metric("Jumlah Total Sekolah", f"{total_schools:,}")
