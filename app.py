import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date, datetime
import pandas as pd

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Laporan Harian - fromthishomeland",
    page_icon="🌿",
    layout="centered",
)

st.title("🌿 Laporan Harian Belanja")
st.caption("fromthishomeland — input real-time ke Google Sheets")

# =========================================================
# KONEKSI KE GOOGLE SHEETS
# =========================================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME = st.secrets["gsheet"]["sheet_name"]          # nama file Google Sheet
WORKSHEET_NAME = st.secrets["gsheet"]["worksheet_name"]   # nama tab/sheet, misal "Laporan Harian Belanja"

HEADERS = [
    "Hari dan Tanggal",
    "Nama Produk",
    "Banyaknya",
    "Harga Pedagang",
    "Harga Vendor",
    "Keuntungan",
]

@st.cache_resource(show_spinner=False)
def get_worksheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sh = client.open(SHEET_NAME)
    try:
        ws = sh.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=10)

    # Pastikan header sudah ada di baris pertama
    existing_header = ws.row_values(1)
    if existing_header != HEADERS:
        ws.update("A1", [HEADERS])

    return ws


def load_data(ws):
    records = ws.get_all_records()
    return pd.DataFrame(records)


# =========================================================
# FORM INPUT
# =========================================================
try:
    ws = get_worksheet()
    connection_ok = True
except Exception as e:
    connection_ok = False
    st.error(
        "Gagal terhubung ke Google Sheets. Periksa kembali secrets.toml "
        "(gcp_service_account & gsheet)."
    )
    st.exception(e)

if connection_ok:
    with st.form("form_laporan", clear_on_submit=True):
        st.subheader("Tambah Data Baru")

        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Hari dan Tanggal", value=date.today())
        with col2:
            nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Kopi Arabika 250g")

        banyaknya = st.number_input("Banyaknya", min_value=0, step=1, value=0)

        col3, col4 = st.columns(2)
        with col3:
            harga_pedagang = st.number_input(
                "Harga Pedagang (modal/beli, per unit)", min_value=0, step=1000, value=0
            )
        with col4:
            harga_vendor = st.number_input(
                "Harga Vendor (jual, per unit)", min_value=0, step=1000, value=0
            )

        keuntungan = (harga_vendor - harga_pedagang) * banyaknya
        st.metric("Keuntungan (otomatis)", f"Rp {keuntungan:,.0f}".replace(",", "."))

        submitted = st.form_submit_button("💾 Simpan ke Google Sheets", use_container_width=True)

        if submitted:
            if not nama_produk:
                st.warning("Nama Produk tidak boleh kosong.")
            else:
                tanggal_str = tanggal.strftime("%d/%m/%Y")
                new_row = [
                    tanggal_str,
                    nama_produk,
                    banyaknya,
                    harga_pedagang,
                    harga_vendor,
                    keuntungan,
                ]
                ws.append_row(new_row, value_input_option="USER_ENTERED")
                st.success(f"Data '{nama_produk}' berhasil disimpan!")
                st.cache_data.clear()

    st.divider()

    # =========================================================
    # TAMPILKAN DATA TERKINI
    # =========================================================
    st.subheader("📊 Data Laporan Terkini")

    df = load_data(ws)

    if df.empty:
        st.info("Belum ada data. Silakan isi form di atas.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

        total_untung = pd.to_numeric(df["Keuntungan"], errors="coerce").sum()
        total_produk = pd.to_numeric(df["Banyaknya"], errors="coerce").sum()

        col_a, col_b = st.columns(2)
        col_a.metric("Total Keuntungan", f"Rp {total_untung:,.0f}".replace(",", "."))
        col_b.metric("Total Barang Terjual", f"{total_produk:,.0f}".replace(",", "."))

    if st.button("🔄 Refresh Data"):
        st.rerun()

st.divider()
st.caption(f"Terakhir dimuat: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")