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
        """Mengatur izin file ke chmod 600 (Hanya owner Read/Write) di Linux."""
        if os.name =='posix':   # Cek apakah OS-nya Linux/Unix
            try:
                # Menjalankan perintah shell: chmod 600 pyvault.db
                subprocess.run(['chmod', '600', self.db_name], check=True)
            except Exception as e:
                print(f"[Warning] Gagal mengatur izin file DB")

    def _create_tables(self):
        """
        Membuat 2 tabel:
        1. security_config: Menyimpan salt dan verifier untuk login
        2. vault_items: Menyimpan password terenkripsi
        """

        # Tabel 1: Security Config (Salt & Verifier)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_config (
                salt BLOB NOT NULL,
                verifier BLOB NOT NULL
            )
        ''')
        
        # Tabel 2: Vault Items (Data Password)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                username TEXT NOT NULL,
                enc_data BLOB NOT NULL,
                nonce BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ''')
        self.conn.commit()
    
    def is_initialized(self):
        """
        Cek apakah program sudah pernah di-setup
        
        Returns:
            bool: True jika sudah ada master password, False jika belum
        """
        self.cursor.execute("SELECT COUNT(*) FROM security_config")
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def save_config(self, salt, verifier):
        """
        Simpan salt dan verifier keamanan saat Setup awal
        Args:
            salt (bytes): Combined salt (master_salt + verifier_salt)
            verifier (bytes): Hash dari master key
        """
        self.cursor.execute("INSERT INTO security_config (salt, verifier) VALUES (?, ?)", (salt, verifier))
        self.conn.commit()

    def get_config(self):
        """ 
        Ambil salt & verifier untuk proses login
        Returns:
            tuple: (salt, verifier) atau None jika belum setup
        """
        self.cursor.execute("SELECT salt, verifier FROM security_config")
        result = self.cursor.fetchone
        return result
    
    def add_item(self, site, username, enc_data, nonce):
        """ 
        Simpan password terenkripsi ke vault
        Args:
            site (str): Nama website/service
            username (str): Username/email
            enc_data (bytes): Password terenkripsi (ciphertext)
            nonce (bytes): untuk dekripsi
        """
        self.cursor.execute("INSERT INTO vault_items (site_name, username, enc_data, nonce) VALUES (?, ?, ?, ?)", (site, username, enc_data, nonce))
        self.conn.commit()

    def get_all_items(self):
        """ 
        Ambil daftar akun untuk ditampilkan di menu (Hanya info umum, bukan passwordnya 
        Returns:
            list: [(id, site_name, username), ...]
        """
        self.cursor.execute("SELECT id, site_name, username FROM vault_items ORDER BY created_at DESC")
        return self.cursor.fetchall()
    
    def get_item_by_id(self, item_id):
        """ Ambil data terenkripsi spesifik untuk di dekripsi nanti"""
        self.cursor.execute("SELECT enc_data, nonce FROM vault_items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()
    
    def delete_item(self, item_id):
        """Hapus item dari vault."""
        self.cursor.execute("DELETE FROM vault_items WHERE id = ?", (item_id))
        self.conn.commit

    def update_item(self, item_id, site, username, enc_data, nonce):
        """Update item yang sudah ada"""
        self.cursor.execute('''UPDATE vault_items SET site_name = ?, username = ?, enc_data = ?, nonce = ? WHERE id = ?''', (site, username, enc_data, nonce, item_id))
        self.conn.commit()

    def close(self):
        self.conn.close()