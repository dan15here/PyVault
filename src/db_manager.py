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
        # chmod 600
        if os.name =='posix':
            try:
                subprocess.run(['chmod', '600', self.db_name], check=True)
            except Exception as e:
                print(f"[Warning] Gagal mengatur izin file DB")

    def _create_tables(self):
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
            )
        ''')
        self.conn.commit()
    
    def is_initialized(self):
        self.cursor.execute("SELECT COUNT(*) FROM security_config")
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def save_config(self, salt, verifier):
        self.cursor.execute("INSERT INTO security_config (salt, verifier) VALUES (?, ?)", (salt, verifier))
        self.conn.commit()

    def get_config(self):
        self.cursor.execute("SELECT salt, verifier FROM security_config")
        result = self.cursor.fetchone()
        return result
    
    def add_item(self, site, username, enc_data, nonce):
        self.cursor.execute("INSERT INTO vault_items (site_name, username, enc_data, nonce) VALUES (?, ?, ?, ?)", (site, username, enc_data, nonce))
        self.conn.commit()

    def get_all_items(self):
        self.cursor.execute("SELECT id, site_name, username FROM vault_items ORDER BY created_at DESC")
        return self.cursor.fetchall()
    
    def get_item_by_id(self, item_id):
        self.cursor.execute("SELECT enc_data, nonce FROM vault_items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()
    
    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM vault_items WHERE id = ?", (item_id,))
        self.conn.commit()

    def update_item(self, item_id, site, username, enc_data, nonce):
        self.cursor.execute('''UPDATE vault_items SET site_name = ?, username = ?, enc_data = ?, nonce = ? WHERE id = ?''', (site, username, enc_data, nonce, item_id))
        self.conn.commit()

    def close(self):
        self.conn.close()