import curses
from .db_manager import DatabaseManager
from .crypto_utils import CryptoManager
from .tui import login_page, create_label_page
from .utils import copy_to_clipboard

class AppController:
    """
    Controller utama untuk menghubungkan semua komponen:
    - TUI (Text User Interface)
    - Database (Storage)
    - Crypto (Encryption/Decryption)
    """

    def __init__(self):
        self.db = DatabaseManager
        self.crypto = CryptoManager
        self.master_key = None
        self.salt = None
    
    def setup_first_time(self, stdscr):
        """
        Setup master password untuk pertama kali
        Flow:
        1. User input master password
        2. Generate salt
        3. Derive key dari password
        4. Create verifier (hash dari key)
        5. Simpan salt + verifier ke database
        """
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