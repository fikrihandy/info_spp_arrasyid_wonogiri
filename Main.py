# ------------ author : @fikrihandy ------------ #
import streamlit as st
import pandas as pd
import google_spreadsheets as gs

# ----------------- Widescreen ----------------- #
st.set_page_config(layout="wide")

st.title("Rekap Biaya Administrasi Ma'had Aly Ar-Rasyid")

try:
    find_id = int(st.text_input('Nomor Induk Mahasantriwati :'))
    find_id_str = repr(find_id)
    angkatan = int(f'{find_id_str[-4]}{find_id_str[-3]}{find_id_str[-2]}{find_id_str[-1]}')
    active_sheet_csv = pd.DataFrame()


    def get_sheet(gid):
        return pd \
            .read_csv(f'{gs.google_spreadsheet}{gid}&single=true&output=csv') \
            .set_index('NIM')


    if angkatan == 2022:
        active_sheet_csv = get_sheet(gs.data_22)
    elif angkatan == 2023:
        active_sheet_csv = get_sheet(gs.data_23)

    active_sheet_dict = active_sheet_csv.to_dict()
    column = []

    for col in active_sheet_csv.columns:
        column.append(col)

    nominal = []

    for i in column:
        if i == 'Nama':
            st.header(f'Nama : {active_sheet_dict[i][find_id]} - (NIM : {find_id}) - (Angkatan : {angkatan})')
        elif i == 'Uang Pangkal':
            if pd.isna(active_sheet_dict[i][find_id]):
                st.error('Belum bayar Uang Pangkal!', icon='❌')
            else:
                st.success(f'Uang Pangkal telah terbayar: {active_sheet_dict[i][find_id]}', icon='✅')

        else:
            nominal.append(active_sheet_dict[i][find_id])

    nominal_show = []
    for i in nominal:
        if pd.isna(i):
            nominal_show.append("BELUM BAYAR")
        else:
            nominal_show.append(i)

    column.remove('Nama')
    column.remove('Uang Pangkal')

    col1, col2, col3 = st.columns(3, gap="large")


    def show_table(title, start_from, end):
        st.subheader(title)
        data = {
            "Pembayaran": column[start_from - 1:end],
            "Nominal": nominal_show[start_from - 1:end]
        }
        df = pd.DataFrame(data)
        df.index += start_from
        st.table(df)


    with col1:
        show_table(title="Semester 1 - 2", start_from=1, end=13)

    with col2:
        show_table(title="Semester 3 - 4", start_from=14, end=26)

    with col3:
        show_table(title="Semester 5 - 6", start_from=27, end=len(column))

except ValueError:
    st.write("Wrong data")
