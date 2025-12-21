import sqlite3
import os
import subprocess

class DatabaseManager:
    def __init__(self, db_name='pyvault.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)  # 1. Koneksi ke SQLite
        self.cursor = self.conn.cursor()
        self._create_tables()                      # 2. Pastikan tabel tersedia
        self._harden_permission()                  # 3. Kunci file database (Security)
    
    def _harden_permission(self):
        """Mengatur izin file ke 600 (Hanya owner Read/Write) di Linux."""
        if os.name =='posix':   # Cek apakah OS-nya Linux/Unix
            try:
                # Menjalankan perintah shell: chmod 600 pyvault.db
                subprocess.run(['chmod', '600', self.db_name], check=True)
            except Exception as e:
                print(f"[Warning] Gagal mengatur izin file DB")

    def _create_tables(self):
        """Tabel Config (Salt & Verifier)"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_config (
                salt BLOB,
                Verifier BLOB
            )
        ''')
        
        """Tabel Vault (Data Password)"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXIST vault_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT
                username Text,
                enc_data BLOB,
                nonce BLOB)
        ''')
        self.conn.commit()
    
    def is_initialized(self):
        """Cek apakah tabel config ada isinya. Kalau 0 berarti aplikasi baru di install."""
        self.cursor.execute("SELECT count(*) FROM security_config")
        return self.cursor.fetchone()[0] > 0
    
    def save_config(self, salt, verifier):
        """Simpan settingan keamanan saat Setup awal"""
        self.cursor.execute("INSERT INTO security_config (salt, verifier) VALUES (?, ?)", (salt, verifier))
        self.conn.commit()

    def get_config(self):
        """ Ambil salt & verifier untuk proses login"""
        self.cursor.execute("SELECT salt, verifier FROM security_config")
        return self.cursor.fetchone()
    
    def add_item(self, site, username, enc_data, nonce):
        """ Simpan password baru yang sudah terenkripsi"""
        self.cursor.execute(
            "INSERT INTO vault_items (site_name, username, enc_data, nonce) VALUES (?, ?, ?, ?)",
            (site, username, enc_data, nonce)
        )
        self.conn.commit()

    def get_all_items(self):
        """ Ambil daftar akun untuk ditampilkan di menu (Hanya info umum, bukan passwordnya """
        self.cursor.execute("SELECT id, site_name, username FROM vault_items")
        return self.cursor.fetchall()
    
    def get_item_by_id(self, item_id):
        """ Ambil data terenkripsi spesifik untuk di dekripsi nanti"""
        self.cursor.execute("SELECT enc_data, nonce FROM vault_items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()