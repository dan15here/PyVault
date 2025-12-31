import curses

LOGO = [
    "╔══════════════════════════════╗",
    "║        P Y V A U L T         ║",
    "║       Password Manager       ║",
    "╚══════════════════════════════╝",
]

# ======================================================
# FIRST TIME SETUP PAGE
# ======================================================
def first_setup_page(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)
    password = ""
    retype_password = ""
    show_password = False
    current_field = 0 
    error_message = ""

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        y = 1
        for line in LOGO:
            if w > len(line) + 2:
                stdscr.addstr(y, 2, line, curses.color_pair(1))
            y += 1
        
        y += 1
        stdscr.addstr(y, 2, "══════ FIRST TIME SETUP ═══════", curses.A_BOLD)
        y += 2
        stdscr.addstr(y, 2, "Create your Master Password")
        y += 1
        stdscr.addstr(y, 2, "(Minimum 8 characters)")
        y += 2

        pwd_display = password if show_password else "*" * len(password)
        highlight1 = "▶" if current_field == 0 else " "
        pwd_y = y
        stdscr.addstr(pwd_y, 2, highlight1, curses.A_BOLD | curses.color_pair(2))
        stdscr.addstr(pwd_y, 4, f"Password        : {pwd_display}")

        retype_display = retype_password if show_password else "*" * len(retype_password)
        highlight2 = "▶" if current_field == 1 else " "
        retype_y = pwd_y + 2
        stdscr.addstr(retype_y, 2, highlight2, curses.A_BOLD | curses.color_pair(2))
        stdscr.addstr(retype_y, 4, f"Retype Password : {retype_display}")

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(retype_y + 2, 4, f"{checkbox} Show Password (TAB)")

        stdscr.addstr(retype_y + 4, 4, "UP/DOWN: Switch | ENTER: Submit | ESC: Exit")

        if error_message:
            stdscr.addstr(retype_y + 6, 4, error_message, curses.A_BOLD | curses.color_pair(3))

        if current_field == 0:
            stdscr.move(pwd_y, 22 + len(password))
        else:
            stdscr.move(retype_y, 22 + len(retype_password))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  
            return None
        elif key == 9:
            show_password = not show_password
        elif key == curses.KEY_UP:
            current_field = 0
            error_message = ""
        elif key == curses.KEY_DOWN:
            current_field = 1
            error_message = ""
        elif key in (10, 13):
            if len(password) < 8:
                error_message = "Password too short! (min 8 characters)"
            elif password != retype_password:
                error_message = "Passwords do not match!"
            elif password == retype_password and len(password) >= 8:
                return password
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if current_field == 0:
                password = password[:-1]
            else:
                retype_password = retype_password[:-1]
            error_message = ""
        elif 32 <= key <= 126:
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

        stdscr.addstr(2, 2, "╔" + "═" * 30 + "╗", curses.color_pair(1))
        stdscr.addstr(3, 2, "║" + "PYVAULT LOGIN".center(30) + "║", curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(4, 2, "╚" + "═" * 30 + "╝", curses.color_pair(1))

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(6, 4, f"Password : {pwd}")

        checkbox = "[✓]" if show_password else "[ ]"
        stdscr.addstr(8, 4, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(10, 4, "ENTER: Login │ ESC: Exit")

        stdscr.move(6, 15 + len(password))
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
