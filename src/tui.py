import curses


# First setup page
def first_setup_page(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)
    password = ""
    retype_password = ""
    show_password = False
    current_field = 0  # 0 = password, 1 = retype password
    error_message = ""

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Header
        stdscr.addstr(2, 2, "=== FIRST TIME SETUP ===", curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(4, 2, "Create your Master Password")
        stdscr.addstr(5, 2, "(Minimum 8 characters)")

        # Password field
        pwd_display = password if show_password else "*" * len(password)
        if current_field == 0:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(8, 4, f"Password        : {pwd_display}")
        if current_field == 0:
            stdscr.attroff(curses.A_REVERSE)

        # Retype password field
        retype_display = retype_password if show_password else "*" * len(retype_password)
        if current_field == 1:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(10, 4, f"Retype Password : {retype_display}")
        if current_field == 1:
            stdscr.attroff(curses.A_REVERSE)

        # Show password checkbox
        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(12, 4, f"{checkbox} Show Password (TAB)")

        # Instructions
        stdscr.addstr(14, 4, "UP/DOWN: Switch Field | ENTER: Submit | ESC: Exit")

        # Error message
        if error_message:
            stdscr.addstr(16, 4, error_message, curses.A_BOLD | curses.color_pair(3))

        # Move cursor to current field
        if current_field == 0:
            stdscr.move(8, 22 + len(password))
        else:
            stdscr.move(10, 22 + len(retype_password))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # ESC
            return None
        elif key == 9:  # TAB - toggle show password
            show_password = not show_password
        elif key == curses.KEY_UP:
            current_field = 0
            error_message = ""
        elif key == curses.KEY_DOWN:
            current_field = 1
            error_message = ""
        elif key in (10, 13):  # ENTER - submit
            if len(password) < 8:
                error_message = "Password too short! (min 8 characters)"
            elif password != retype_password:
                error_message = "Passwords do not match!"
            elif password == retype_password and len(password) >= 8:
                return password
        elif key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace
            if current_field == 0:
                password = password[:-1]
            else:
                retype_password = retype_password[:-1]
            error_message = ""
        elif 32 <= key <= 126:  # Printable characters
            if current_field == 0:
                password += chr(key)
            else:
                retype_password += chr(key)
            error_message = ""


# ======================================================
# LOGIN PAGE
# ======================================================
def login_page(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)
    password = ""
    show_password = False

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(2, 2, "PYVAULT LOGIN", curses.A_BOLD | curses.color_pair(1))

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(5, 4, f"Password : {pwd}")

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(7, 4, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(9, 4, "ENTER Login | ESC Exit")

        stdscr.move(5, 15 + len(password))
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return None  
        elif key == 9:
            show_password = not show_password
        elif key in (10, 13):
            if password:
                return password
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            password = password[:-1]
        elif 32 <= key <= 126:
            password += chr(key)

# ======================================================
# CREATE / EDIT LABEL PAGE
# ======================================================
def create_label_page(stdscr, preset_data=None):
    curses.curs_set(1)
    stdscr.keypad(True)

    label = preset_data["label"] if preset_data else ""
    site = preset_data["site"] if preset_data else ""
    username = preset_data["username"] if preset_data else ""
    password = preset_data["password"] if preset_data else ""
    description = preset_data["description"] if preset_data else ""

    fields = ["label", "site", "username", "password", "description"]
    current = 0
    show_password = False

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "EDIT LABEL" if preset_data else "CREATE LABEL"
        stdscr.addstr(1, 2, title, curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(2, 2, "-" * 40)

        stdscr.addstr(5, 4, f"Label       : {label}")
        stdscr.addstr(7, 4, f"Site        : {site}")
        stdscr.addstr(9, 4, f"Username    : {username}")

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(11, 4, f"Password    : {pwd}")

        stdscr.addstr(13, 4, "Description :")
        lines = description.split("\n") if description else [""]
        for i, line in enumerate(lines[:3]):
            stdscr.addstr(14 + i, 18, line[: w - 20])

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(h - 4, 4, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(h - 2, 2, "CTRL+N Save | UP/DOWN Move | ESC Back")

        field = fields[current]
        y_map = {"label": 5, "site": 7, "username": 9, "password": 11}
        if field == "description":
            y = 14 + len(lines) - 1
            x = 18 + len(lines[-1])
        else:
            y = y_map[field]
            x = 20 + len(eval(field))

        stdscr.move(min(y, h - 1), min(x, w - 1))
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return None
        elif key == 9:
            show_password = not show_password
        elif key == curses.KEY_UP:
            current = (current - 1) % len(fields)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(fields)
        elif key == 14:
            if label and site and username and password:
                return {
                    "label": label,
                    "site": site,
                    "username": username,
                    "password": password,
                    "description": description
                }
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if field == "label": label = label[:-1]
            elif field == "site": site = site[:-1]
            elif field == "username": username = username[:-1]
            elif field == "password": password = password[:-1]
            elif field == "description": description = description[:-1]
        elif key in (10, 13) and field == "description":
            description += "\n"
        elif 32 <= key <= 126:
            if field == "label": label += chr(key)
            elif field == "site": site += chr(key)
            elif field == "username": username += chr(key)
            elif field == "password": password += chr(key)
            elif field == "description": description += chr(key)


# ======================================================
# DASHBOARD
# ======================================================
def dashboard_page(stdscr):
    curses.curs_set(0)

    items = [{
        "label": "akun steam",
        "site": "www.steam.com",
        "username": "GodOfHyperdeath",
        "password": "chara1234",
        "description": "Akun utama"
    }]

    current = 0
    message = ""

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, "DASHBOARD", curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * 40)

        y = 4
        for i, item in enumerate(items):
            if i == current:
                stdscr.attron(curses.A_REVERSE)

            stdscr.addstr(y, 4, f"Label    : {item['label']}")
            stdscr.addstr(y + 1, 4, f"Site     : {item['site']}")
            stdscr.addstr(y + 2, 4, f"Username : {item['username']}")
            stdscr.addstr(y + 3, 4, f"Password : {'*' * len(item['password'])}")

            if i == current:
                stdscr.attroff(curses.A_REVERSE)

            y += 6

        stdscr.addstr(h - 3, 2, "CTRL+N New | E Edit | O Copy | ESC Back")
        if message:
            stdscr.addstr(h - 2, 2, message)

        stdscr.refresh()
        key = stdscr.getch()
        message = ""

        if key == curses.KEY_UP:
            current = (current - 1) % len(items)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(items)
        elif key == 14:
            new = create_label_page(stdscr)
            if new:
                items.append(new)
                current = len(items) - 1
        elif key in (ord("e"), ord("E")):
            edited = create_label_page(stdscr, items[current])
            if edited:
                items[current] = edited
        elif key in (ord("o"), ord("O")):
            message = f"Password copied: {items[current]['password']}"
        elif key == 27:
            return
            