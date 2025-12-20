import sqlite3
import os
import subprocess

class DatabaseManager:
    def __init__(self, db_name='pyvault.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._harden_permission()
    
    def _harden_permission(self):
        """Mengatur izin file ke 600 (Hanya owner Read/Write) di Linux."""
        if os.name =='posix':
            try:
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
        
        """Tabel Vault (Data Password"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXIST vault_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT
                username Text,
                enc_data BLOB,
                nonce BLOB)
        ''')
        self.conN.commmit()