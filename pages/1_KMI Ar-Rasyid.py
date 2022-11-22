# ------------ author : @fikrihandy ------------ #
import streamlit as st
import pandas as pd
import google_spreadsheets as gs

# ----------------- Set Page ----------------- #
st.set_page_config(page_title="Keuangan KMI Ar-Rasyid", layout="wide")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Rekap Biaya Administrasi KMI Ar-Rasyid")

angkatan = st.selectbox(
    'Angkatan Tahun:',
    range(2018, 2023), index=3)

st.write('Tahun masuk:', angkatan)

jenis_kelamin = st.selectbox(
    'Kelas:',
    ('Putra', 'Putri'), key='selected_jenis_kelamin')

st.write(f'KMI Ar-Rasyid {jenis_kelamin}')

link = f'{gs.kmi_s_id}{gs.data_kmi[angkatan][jenis_kelamin]}&single=true&output=csv'
csv = pd.read_csv(link)
name_list = csv['Nama'].tolist()

with st.form(key="nama_dan_kode"):
    st.write("This is inside the container")
    nama_santri = st.selectbox(
        'Nama:', name_list, key='selected_name')
    santri_index = csv[csv['Nama'] == nama_santri].index.values
    kode = st.text_input("Masukkan kode = ")

    if st.form_submit_button() and kode == str(csv.iloc[santri_index]['NIM'].item()):
        show_data = csv.loc[santri_index].to_dict()
        # st.write(show_data)

        # print(show_data)

        column_spp = []

        for col in show_data:
            if col == 'Nama' or col[0] == '!' or col == "NIM":
                continue
            else:
                column_spp.append(col)

        nominal = []
        santri_index = int(santri_index)
        for i in column_spp:
            if pd.isna(show_data[i][santri_index]) or show_data[i][santri_index] == ' - 🔵 𝘒𝘦𝘵. = ':
                nominal.append("❌ BELUM BAYAR")
            else:
                nominal.append(show_data[i][santri_index])

        st.subheader(f"Nama : {show_data['Nama'][santri_index]}")
        st.write(f"Nomor Induk : {show_data['!No Induk'][santri_index]}")

        uang_gedung = show_data['!Nominal Gedung'][santri_index]
        perlengkapan = show_data['!Nominal Perlengkapan'][santri_index]
        seragam = show_data['!Nominal Seragam'][santri_index]
        ket_gedung = show_data['!Ket Gedung'][santri_index]
        ket_perlengkapan = show_data['!Ket Perlengkapan'][santri_index]
        ket_seragam = show_data['!Ket Seragam'][santri_index]

        belum_bayar = "❌ BELUM BAYAR"
        belum = "Belum tersedia"

        if pd.isna(show_data['!Nominal Gedung'][santri_index]):
            uang_gedung = belum_bayar
            ket_gedung = belum

        if pd.isna(show_data['!Nominal Perlengkapan'][santri_index]):
            perlengkapan = belum_bayar
            ket_perlengkapan = belum

        if pd.isna(show_data['!Nominal Seragam'][santri_index]):
            seragam = belum_bayar
            ket_seragam = belum

        d = {'Nominal': [uang_gedung, perlengkapan, seragam],
             'Keterangan': [ket_gedung, ket_perlengkapan, ket_seragam]}
        data_uang_daftar = pd.DataFrame(data=d, index=['Uang Gedung', 'Perlengkapan', 'Seragam'])

        st.table(data_uang_daftar)

        col1, col2, col3 = st.columns(3)

        df = pd.DataFrame(nominal, index=column_spp, columns=["Nominal"])
        # st.table(df)

        with col1:
            st.subheader("Kelas 1")
            st.table(df.iloc[0:14])

        with col2:
            st.subheader("Kelas 2")
            st.table(df.iloc[14:28])

        with col3:
            st.subheader("Kelas 3")
            st.table(df.iloc[28:42])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.subheader("Kelas 4")
            st.table(df.iloc[42:56])

        with col5:
            st.subheader("Kelas 5")
            st.table(df.iloc[56:70])

        with col6:
            st.subheader("Kelas 6")
            st.table(df.iloc[70:84])
