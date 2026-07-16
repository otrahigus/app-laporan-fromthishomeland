# 🌿 Laporan Harian Belanja — fromthishomeland

Aplikasi Streamlit untuk mengisi Laporan Harian Belanja secara **real-time**, langsung tersimpan ke **Google Sheets**. Cocok dipakai dari HP atau laptop, tanpa perlu buka Google Sheets manual.

Kolom yang diisi:
`Hari dan Tanggal | Nama Produk | Banyaknya | Harga Pedagang | Harga Vendor | Keuntungan (otomatis)`

---

## 1. Siapkan Google Sheet

1. Buka Google Sheets, buat/pakai spreadsheet yang sudah ada (misalnya yang di screenshot kamu: **"Laporan Harian Belanja"**).
2. Pastikan ada satu sheet/tab dengan nama yang sama (atau nama lain, nanti disesuaikan di secrets).
3. Catat **nama file spreadsheet** (bukan URL) — ini yang dipakai di `sheet_name`.

## 2. Buat Service Account Google Cloud (agar app bisa akses Sheets)

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat project baru (atau pakai yang sudah ada).
3. Aktifkan API berikut di **APIs & Services > Library**:
   - **Google Sheets API**
   - **Google Drive API**
4. Buka **APIs & Services > Credentials > Create Credentials > Service Account**.
5. Beri nama bebas, klik **Create and Continue**, lalu **Done**.
6. Klik service account yang baru dibuat → tab **Keys** → **Add Key > Create new key** → pilih **JSON** → download.
7. File JSON ini berisi semua kredensial yang dibutuhkan (`private_key`, `client_email`, dll).

## 3. Bagikan Google Sheet ke Service Account

1. Buka file JSON tadi, salin nilai `client_email` (contoh: `nama@project.iam.gserviceaccount.com`).
2. Buka Google Sheet kamu → klik **Share/Bagikan** → tempel email tsb → beri akses **Editor**.

> Tanpa langkah ini, aplikasi tidak akan bisa menulis data walau kredensial benar.

## 4. Isi `secrets.toml`

1. Salin `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`.
2. Isi bagian `[gsheet]` dengan nama spreadsheet & nama worksheet/tab kamu.
3. Isi bagian `[gcp_service_account]` dengan nilai-nilai dari file JSON di langkah 2 (cukup copy-paste tiap field, perhatikan `private_key` tetap dalam format `"-----BEGIN...-----\n...\n-----END...-----\n"`).

⚠️ **Jangan pernah commit `secrets.toml` ke GitHub.** File ini sudah otomatis diabaikan lewat `.gitignore`.

## 5. Jalankan secara lokal (opsional, untuk uji coba)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 6. Upload ke GitHub

```bash
git init
git add .
git commit -m "Laporan harian fromthishomeland"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

(Pastikan `secrets.toml` **tidak** ikut ter-push — cek dengan `git status`.)

## 7. Deploy ke Streamlit Community Cloud (gratis, real-time)

1. Buka [share.streamlit.io](https://share.streamlit.io) → login dengan GitHub.
2. Klik **New app** → pilih repo GitHub kamu → branch `main` → file utama `app.py`.
3. Sebelum/atau setelah deploy, buka menu **Settings > Secrets** pada app tsb.
4. Tempel **seluruh isi** `secrets.toml` (yang sudah kamu isi lengkap) ke kotak Secrets itu.
5. Klik **Save** → aplikasi otomatis restart dan langsung bisa dipakai dari mana saja.

Setelah itu, setiap kali kamu isi form di app dan klik **Simpan**, data langsung masuk ke Google Sheet secara real-time — dan siapa pun yang buka link app-nya bisa mengisi laporan dari HP/laptop tanpa perlu buka Sheets.

---

## Struktur Project

```
laporan-harian-app/
├── app.py                          # Aplikasi utama Streamlit
├── requirements.txt                # Dependencies
├── .gitignore                      # Agar secrets tidak ter-commit
├── .streamlit/
│   └── secrets.toml.example        # Contoh format secrets (isi lalu rename)
└── README.md
```

## Kustomisasi

- Ubah kolom di `HEADERS` (dalam `app.py`) jika struktur laporan berubah.
- Ubah rumus `keuntungan` di `app.py` jika logika untung-rugi kamu berbeda (saat ini: `(Harga Vendor - Harga Pedagang) x Banyaknya`).
- Tambahkan filter tanggal/produk di bagian "Data Laporan Terkini" jika data sudah banyak.