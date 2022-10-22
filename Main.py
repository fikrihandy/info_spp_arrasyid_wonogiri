# ------------ author : @fikrihandy ------------ #
import streamlit as st
import pandas as pd
import google_spreadsheets as gs

# ----------------- Set Page ----------------- #
st.set_page_config(page_title="Keuangan Ma'had Aly Ar-Rasyid", layout="wide")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Rekap Biaya Administrasi Ma'had Aly Ar-Rasyid")


def nim_salah():
    st.write("---")
    st.error(f"NIM salah. Harap periksa kembali. Jika terdapat masalah silakan hubungi Admin.")
    with st.expander(f"Admin Bag. Keuangan {gs.bag_keuangan}"):
        f'HP / WhatsApp: {gs.phone_number}'


def welcome():
    home = 'https://arrasyid.ponpes.id/'
    donasi = 'https://donasi.arrasyid.ponpes.id/'
    psb = 'https://psb.arrasyid.ponpes.id/'
    st.write(f"> [Web Ar-Rasyid]({home}) * [Donasi]({donasi}) * [Penerimaan Santri Baru]({psb})")
    col4, col5 = st.columns([2, 1])
    col4.image(image=gs.img, use_column_width=True)
    col5.image(image=gs.img2, use_column_width=True, caption='Penerimaan Santri Baru 2022/2023')


try:
    find_id = int(st.text_input(
        label='Nomor Induk Mahasantriwati :',
        help="Masukkan NIM lalu tekan enter."
    ))
    find_id_str = repr(find_id)
    angkatan = int(f'{find_id_str[0]}{find_id_str[1]}')
    active_sheet_csv = pd.DataFrame()


    def get_sheet(gid):
        return pd \
            .read_csv(f'{gs.s_id}{gid}&single=true&output=csv') \
            .set_index('NIM')


    if angkatan == 21:
        active_sheet_csv = get_sheet(gs.data_21)
    elif angkatan == 22:
        active_sheet_csv = get_sheet(gs.data_22)
    elif angkatan == 23:
        active_sheet_csv = get_sheet(gs.data_23)

    active_sheet_dict = active_sheet_csv.to_dict()
    column = []

    for col in active_sheet_csv.columns:
        column.append(col)

    nominal = []

    for i in column:
        nominal.append(active_sheet_dict[i][find_id])
        if i == 'Nama':
            st.header(f'Nama : {active_sheet_dict[i][find_id]}')
        elif i == 'Uang Pangkal':
            if pd.isna(active_sheet_dict[i][find_id]) or active_sheet_dict[i][find_id] == ' - 🔵 𝘒𝘦𝘵. = ':
                st.error('Belum bayar Uang Pangkal!', icon='❌')
            else:
                st.success(f'Uang Pangkal telah terbayar: {active_sheet_dict[i][find_id]}', icon='✅')

    nominal_show = []
    for i in nominal:
        if pd.isna(i) or i == ' - 🔵 𝘒𝘦𝘵. = ':
            nominal_show.append("❌ BELUM BAYAR")
        else:
            nominal_show.append(i)

    if nominal_show:

        def show_table(title, start, end):
            data = {"Nominal": nominal_show}
            st.subheader(title)
            df = pd.DataFrame(data, index=column)
            filtered_df = []
            for x in column:
                if x == 'Nama' or x == 'Uang Pangkal' or x[0] == '!':
                    filtered_df.append(x)
            df = df.drop(filtered_df)
            df = df.iloc[start - 1:end]
            st.table(df)


        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            show_table(title="Semester 1 - 2", start=1, end=13)

        with col2:
            show_table(title="Semester 3 - 4", start=14, end=26)

        with col3:
            show_table(title="Semester 5 - 6", start=27, end=len(column))

        if st.button(label='Refresh data'):
            active_sheet_csv = pd.DataFrame()

        st.markdown("**_Informasi: Data akan otomatis update sesuai server setelah ± 5 menit_**")
        st.write(f"Admin Bagian Keuangan: {gs.phone_number} ({gs.bag_keuangan})")
    else:
        nim_salah()
except ValueError:
    welcome()

except KeyError:
    nim_salah()

except IndexError:
    nim_salah()
