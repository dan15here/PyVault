import curses
from .db_manager import DatabaseManager
from .crypto_utils import CryptoManager
from .tui import login_page, create_label_page, first_setup_page
from .utils import copy_to_clipboard, validate_password_strength
from .logger import get_logger

LOGO = [
    "╔══════════════════════════════╗",
    "║        P Y V A U L T         ║",
    "║       Password Manager       ║",
    "╚══════════════════════════════╝",
]

DIVIDER = "─" * 42

class AppController:
    def __init__(self):
        self.db = DatabaseManager()
        self.crypto = CryptoManager()
        self.master_key = None
        self.salt = None
        self.logger = get_logger()
    
    def setup_first_time(self, stdscr):
        stdscr.clear()
        stdscr.addstr(2, 2, "═══ FIRST TIME SETUP ═══", curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(4, 2, "Create Master Password")
        stdscr.addstr(5, 2, "(Minimum 8 characters)")
        stdscr.addstr(7, 2, "This password will protect all your data.")
        stdscr.addstr(8, 2, "If you forget your password, your data will be lost!")
        stdscr.addstr(9, 2, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()

        master_password = first_setup_page(stdscr)

        if not master_password:
            stdscr.clear()
            stdscr.addstr(5, 2, "Setup cancelled!", curses.A_BOLD | curses.color_pair(3))
            stdscr.addstr(7, 2, "Press any key to exit...")
            stdscr.refresh()
            stdscr.getch()
            return False

        # Validasi password strength
        is_valid = validate_password_strength(master_password)
        if not is_valid:
            stdscr.clear()
            stdscr.addstr(5, 2, "Password does not meet requirements!", curses.A_BOLD | curses.color_pair(3))
            stdscr.addstr(7, 2, "Password must contain:")
            stdscr.addstr(8, 4, "- Minimal 8 characters")
            stdscr.addstr(9, 4, "- Uppercase letter (A-Z)")
            stdscr.addstr(10, 4, "- Lowercase letter (a-z)")
            stdscr.addstr(11, 4, "- Number (0-9)")
            stdscr.addstr(12, 4, "- Symbol (!@#$%...)")
            stdscr.addstr(14, 2, "Press any key to try again...", curses.A_BOLD)
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
        stdscr.addstr(5, 2, "Setup completed!", curses.A_BOLD | curses.color_pair(2))
        stdscr.addstr(7, 2, "Press any key to continue...", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        self.logger.log_first_setup(True)
        return True

    def verify_master_password(self, stdscr):
        config = self.db.get_config()
        if not config:
            stdscr.clear()
            stdscr.addstr(5, 2, "No config found!", curses.A_BOLD | curses.color_pair(3))
            stdscr.addstr(7, 2, "Press any key to exit...", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            return False

        combined_salt, stored_verifier = config
        self.salt = combined_salt[:16]
        verifier_salt = combined_salt[16:32]

        master_password = login_page(stdscr)
        if not master_password:return False

        self.master_key = self.crypto.derive_key(master_password, self.salt)

        computed_verifier = self.crypto.hash_verifier(self.master_key, verifier_salt)

        if computed_verifier != stored_verifier:
            stdscr.clear()
            stdscr.addstr(5, 2, "Invalid Password", curses.A_BOLD | curses.color_pair(3))
            stdscr.addstr(7, 2, "Press any key to exit...")
            stdscr.refresh()
            stdscr.getch()
            self.logger.log_login(False)
            return False
        self.logger.log_login(True)
        return True

    def load_vault_items(self):
        items = []
        db_items = self.db.get_all_items()
        for item_id, site_name, username, description in db_items:
            result = self.db.get_item_by_id(item_id)
            if result:
                enc_data, nonce = result
                try:
                    password = self.crypto.decrypt_data(self.master_key, enc_data, nonce)
                    items.append({
                        "id": item_id,
                        "site_name": site_name,
                        "username": username,
                        "password": password,
                        "description": description or ""
                    })
                except Exception as e:
                    print(f"Error decrypting data: {e}")
        return items

    def save_new_item(self, item_data):
        enc_data, nonce = self.crypto.encrypt_data(self.master_key, item_data['password'])
        self.db.add_item(
            item_data['site'],
            item_data['username'],
            enc_data,
            nonce,
            item_data.get('description', '')
        )
        self.logger.log_add_item(item_data['site'])

    def delete_item(self, item_id):
        self.db.delete_item(item_id)

    def update_item(self, item_id, item_data):
        enc_data, nonce = self.crypto.encrypt_data(self.master_key, item_data['password'])
        self.db.update_item(
            item_id,
            item_data['site'],
            item_data['username'],
            enc_data,
            nonce,
            item_data.get('description', '')
        )

    def view_item_detail(self, stdscr, item):
        curses.curs_set(0)
        show_password = False
        
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            stdscr.addstr(1, 2, "ITEM DETAIL", curses.A_BOLD)
            stdscr.addstr(2, 2, "-" * 40)
            
            stdscr.addstr(4, 4, f"Site     : {item['site_name']}")
            stdscr.addstr(6, 4, f"Username : {item['username']}")
            
            pwd = item['password'] if show_password else '*' * len(item['password'])
            stdscr.addstr(8, 4, f"Password : {pwd}")

            desc = item['description'] if show_password else '*' * len(item['description'])
            stdscr.addstr(10, 4, f"Description : {desc}")
            
            checkbox = "[x]" if show_password else "[ ]"
            stdscr.addstr(12, 4, f"{checkbox} Show Password (TAB)")
            
            stdscr.addstr(h - 2, 2, "TAB Toggle Password | ESC Back")
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if key == 27: 
                return
            elif key == 9:  
                show_password = not show_password

    def run_main_menu(self, stdscr):
        curses.curs_set(0)
        menu = ["View Dashboard", "Add New Account", "Exit"]
        current = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            y = 1
            for line in LOGO:
                if w > len(line) + 2:
                    stdscr.addstr(y, 2, line, curses.color_pair(1))
                y += 1
            
            stdscr.addstr(y, 2, "══════════ MAIN MENU ══════════", curses.A_BOLD)
            y += 2

            # menu items
            for i, item in enumerate(menu):
                menu_y = y + i
                if i == current:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(menu_y, 4, f" ▶ {item} ")
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(menu_y, 4, f"   {item}")

            # Footer
            footer = "UP/DOWN:Navigate ENTER:Select"
            if w > len(footer) + 4:
                stdscr.addstr(h - 2, 2, footer)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP:
                current = (current - 1) % len(menu)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(menu)
            elif key in (10, 13):  # ENTER
                if menu[current] == "View Dashboard":
                    self.run_dashboard(stdscr)
                elif menu[current] == "Add New Account":
                    new_item = create_label_page(stdscr)
                    if new_item:
                        self.save_new_item(new_item)
                elif menu[current] == "Exit":
                    return
            elif key == 27: 
                return

    def run_dashboard(self, stdscr):
        curses.curs_set(0)
        items = self.load_vault_items()
        current = 0
        message = ""

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            stdscr.addstr(1, 2, "╔" + "═" * 40 + "╗", curses.color_pair(1))
            stdscr.addstr(2, 2, "║" + "PYVAULT DASHBOARD".center(40) + "║", curses.A_BOLD | curses.color_pair(1))
            stdscr.addstr(3, 2, "╚" + "═" * 40 + "╝", curses.color_pair(1))

            # Display items
            if not items:
                stdscr.addstr(5, 4, "NO DATA FOUND")
                stdscr.addstr(7, 4, "Press CTRL+N to add your first account")
            else:
                y = 4
                for i, item in enumerate(items):
                    # Highlight item saat ini.
                    if i == current:
                        stdscr.attron(curses.A_REVERSE)

                    stdscr.addstr(y, 4, f"Site : {item['site_name']}")
                    stdscr.addstr(y + 1, 4, f"Username : {item['username']}")
                    stdscr.addstr(y + 2, 4, f"Password : {'*' * len(item['password'])}")

                    if i == current:
                        stdscr.attroff(curses.A_REVERSE)

                    y += 5
            
            footer = "ENTER:View E:Edit C:Copy D:Del ^N:Add ESC:Exit"
            if w > len(footer) + 4:
                stdscr.addstr(h - 3, 2, footer)

            # Status message
            if message:
                msg = message[:w-4] if len(message) > w-4 else message
                stdscr.addstr(h - 2, 2, msg, curses.A_BOLD | curses.color_pair(2))
            
            stdscr.refresh()
            key = stdscr.getch()
            message = ""

            # Navigation
            if key == curses.KEY_UP and items:
                current = (current - 1) % len(items)
            elif key == curses.KEY_DOWN and items:
                current = (current + 1) % len(items)
            
            # View detail (ENTER)
            elif key in (10, 13) and items:
                self.logger.log_view_item(items[current]['site_name'])
                self.view_item_detail(stdscr, items[current])
            
            # Edit item
            elif key in (ord('e'), ord('E')) and items:
                edited_item = create_label_page(stdscr, {
                    "label": items[current].get('site_name', ''),
                    "site": items[current].get('site_name', ''),
                    "username": items[current].get('username', ''),
                    "password": items[current].get('password', ''),
                    "description": ""
                })
                if edited_item:
                    self.update_item(items[current]['id'], edited_item)
                    items = self.load_vault_items()
                    message = "Item updated!"
                    self.logger.log_edit_item(edited_item['site'])
            
            # Add new item
            elif key == 14:     # CTRL+N
                new_item = create_label_page(stdscr)
                if new_item:
                    self.save_new_item(new_item)
                    items = self.load_vault_items()
                    current = len(items) - 1
                    message = "Account saved!"

            # Copy Password
            elif key in (ord('c'), ord('C')) and items:
                if copy_to_clipboard(items[current]['password']):
                    message = "Password copied! (auto-clear in 15s)"
                    self.logger.log_copy_password(items[current]['site_name'])
                else:
                    message = "Copy failed (pyperclip not installed)"

            # Delete item
            elif key in (ord('d'), ord('D')) and items:
                stdscr.addstr(h - 2, 2, "Delete this item? (y/n)", curses.A_BOLD)
                stdscr.refresh()
                confirm = stdscr.getch()

                if confirm in (ord('y'), ord('Y')):
                    site_name = items[current]['site_name']
                    self.delete_item(items[current]['id'])
                    items = self.load_vault_items()
                    message = "Item deleted!"
                    self.logger.log_delete_item(site_name)
                
                if current >= len(items) and items:
                    current = len(items) - 1
                elif not items:
                    current = 0

            # Exit
            elif key == 27:return

    def close(self):
        self.logger.log_app_exit()
        self.db.close()
        self.master_key = None 
        self.salt = None