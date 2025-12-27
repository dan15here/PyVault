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