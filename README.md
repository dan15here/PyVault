# 🔐 PyVault - Password Manager

Aplikasi **Password Manager** berbasis terminal (CLI) yang aman untuk menyimpan dan mengelola kredensial akun Anda. Dibangun menggunakan Python dengan antarmuka TUI (Text User Interface) yang interaktif.

---

## ✨ Fitur Utama

- 🔒 **Enkripsi Kuat** - Menggunakan algoritma Argon2 untuk hashing password dan Cryptography untuk enkripsi data
- 🖥️ **Antarmuka Terminal Interaktif** - Interface berbasis curses yang mudah digunakan
- 📋 **Copy ke Clipboard** - Salin password langsung ke clipboard dengan sekali tekan
- 🔍 **Pencarian & Filter** - Temukan kredensial dengan cepat berdasarkan label
- ✏️ **CRUD Lengkap** - Tambah, lihat, edit, dan hapus entri password
- 📝 **Logging** - Pencatatan aktivitas untuk keamanan
- 🛡️ **Validasi Password** - Memastikan master password memenuhi kriteria keamanan

---

## 📋 Persyaratan Sistem

- **Python**: 3.8 atau lebih tinggi
- **OS**: Windows, Linux, atau macOS
- **Dependencies**: Lihat `requirements.txt`

---

## 🚀 Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd tugas_pbl_kel2
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Cara Penggunaan

### Menjalankan Aplikasi
```bash
python main.py
```

### Pertama Kali Menggunakan
1. Aplikasi akan meminta Anda membuat **Master Password**
2. Master Password harus memenuhi kriteria:
   - Minimal 8 karakter
   - Mengandung huruf besar dan kecil
   - Mengandung angka
   - Mengandung simbol khusus

### Menu Utama
- **Dashboard** - Lihat semua kredensial tersimpan
- **Add New** - Tambah entri password baru
- **Search** - Cari kredensial berdasarkan label
- **Exit** - Keluar dari aplikasi

### Navigasi
- Gunakan **Arrow Keys** (↑/↓) untuk navigasi menu
- Tekan **Enter** untuk memilih
- Tekan **ESC** atau **Q** untuk kembali

---

## 📁 Struktur Proyek

```
tugas_pbl_kel2/
├── main.py              # Entry point aplikasi
├── requirements.txt     # Daftar dependencies
├── README.md            # Dokumentasi proyek
└── src/
    ├── app_controller.py  # Logic utama aplikasi
    ├── crypto_utils.py    # Enkripsi & dekripsi
    ├── db_manager.py      # Manajemen database
    ├── tui.py             # Komponen UI terminal
    ├── utils.py           # Fungsi utilitas
    └── logger.py          # Sistem logging
```

---

## 🔧 Dependencies

| Package | Versi | Fungsi |
|---------|-------|--------|
| `argon2-cffi` | 23.1.0 | Hashing password dengan Argon2 |
| `cryptography` | 41.0.7 | Enkripsi/dekripsi data |
| `pyperclip` | 1.8.2 | Copy ke clipboard |
| `windows-curses` | 2.3.3 | Support curses di Windows |

---

## 👥 Anggota Kelompok 2

| No | Nama | NIM |
|----|------|-----|
| 1 | Muhammad Danish | 4332511020 |
| 2 | Arya Deva Bahari | 4332511021 |
| 3 | M Maulana Alpidie Deputra | 4332511017 |

---

## 📚 Mata Kuliah

- **Mata Kuliah**: Algoritma dan Pemrograman
- **Program Studi**: Teknik Informatika
- **Institusi**: Politeknik Negeri Batam
- **Semester**: 1 (Ganjil)
- **Tahun Ajaran**: 2025/2026

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas akademik (Project Based Learning) di Politeknik Negeri Batam.

---

<p align="center">
  <b>🔐 PyVault - Secure Your Digital Life 🔐</b>
</p>
