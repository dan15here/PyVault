import curses
from .db_manager import DatabaseManager
from .crypto_utils import CryptoManager
from .tui import login_page, create_label_page
from .utils import copy_to_clipboard

class AppController:
    def __init__(self):
        self.db = DatabaseManager
        self.crypto = CryptoManager
        self.master_key = None
        self.salt = None
    
    def setup_first_time(self, stdscr):
        stdscr.clear()
        stdscr.addstr(2, 2, "=== FIRST TIME SETUP ===", curses.A_BOLD)
        stdscr.addstr(4, 2, "Buat Master Password Anda")
        stdscr.addstr(5, 2, "(minimum 8 karakter)")
        stdscr.addstr(7, 2, "Password ini akan mengamankan SEMUA data anda.")
        stdscr.addstr(8, 2, "Jika anda lupa password, data anda TIDAK BISA dipulihkan!")
        stdscr.refresh()
        stdscr.getch()

        master_password = login_page(stdscr)

        if not master_password:
            stdscr.clear()
            stdscr.addstr(5, 2, "Setup dibatalkan.", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            return False

        # Validated password length
        if len(master_password) < 8:
            stdscr.clear()
            stdscr.addstr(5, 2, "Password terlalu pendek!.", curses.A_BOLD)
            stdscr.addstr(7, 2, "Password minimal 8 karakter.", curses.A_BOLD)
            stdscr.addstr(9, 2, "Tekan apapun untuk kembali.....", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            return self.setup_first_time(stdscr)

        # Generate salt and master key
        self.salt = self.crypto.generate_salt()
        self.master_key = self.crypto.derive_key(master_password, self.salt)

        # Buat verifier untuk login check
        verifier_salt = self.crypto.generate_salt()
        verifier = self.crypto.hash_verifier(self.master_key, verifier_salt)

        # Gabungkan 2 salt (master + verifier)
        combined_salt = self.salt + verifier_salt
        self.db.save_config(combined_salt, verifier)

        stdscr.clear()
        stdscr.addstr(5, 2, "Setup berhasil!", curses.A_BOLD)
        stdscr.addstr(7, 2, "Tekan apapun untuk melanjutkan.....", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()

        return True

    def verify_master_password(self, stdscr, master_password):
        # Load config dari database
        config = self.db.get_config()
        if not config:
            stdscr.clear()
            stdscr.addstr(5, 2, "Tidak ada config ditemukan.", curses.A_BOLD)
            stdscr.addstr(7, 2, "Tekan apapun untuk melanjutkan.....", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            return False

        combined_salt, stored_verifier = config
        self.salt = combined_salt[:16]
        verifier_salt = combined_salt[16:32]

        # Login page
        master_password = login_page(stdscr)

        if not master_password:
            return False

    def load_vault_items(self):
        items = []
        db_items = self.db.get_all_items()
        for item_id, site_name, username, in db_items:
            result = self.db.get_item_by_id(item_id)
            if result:
                enc_data, nonce = result
                try:
                    password = self.crypto.decrypt_data(self.master_key, enc_data, nonce)
                    items.append({
                        "id": item_id,
                        "site_name": site_name,
                        "username": username,
                        "password": password
                    })
                except Exception as e:
                    print(f"Error decrypting data: {e}")
        return items

    def save_new_item(self, item_data):
        # Enkripsi password
        enc_data, nonce = self.crypto.encrypt_data(self.master_key, item_data['password'])
        # Simpan ke database
        self.db.add_item(
            item_data['site'],
            item_data['username'],
            enc_data,
            nonce
        )

    def run_dashboard(self, stdscr):
        curses.curs_set(0)
        items = self.load_vault_items()
        current = 0
        message = ""

    def run_dashboard(self, stdscr):
        stdscr.clear()
        h, w = stdscr.getmaxyx()


    def close(self):
        self.db.close()
        self.master_key = None  # Clear dari memory
        self.salt = None