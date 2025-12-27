import curses

# ======================================================
# LOGIN PAGE
# ======================================================
def login_page(stdscr):
    curses.curs_set(1)
    password = ""
    show_password = False

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(2, 2, "PYVAULT LOGIN", curses.A_BOLD)

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(5, 4, f"Password : {pwd}")

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(7, 4, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(9, 4, "ENTER Login | ESC Exit")

        stdscr.move(5, 15 + len(password))
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return False
        elif key == 9:
            show_password = not show_password
        elif key in (10, 13):
            if password:
                return True
        elif key in (curses.KEY_BACKSPACE, 127):
            password = password[:-1]
        elif 32 <= key <= 126:
            password += chr(key)


# ======================================================
# CREATE / EDIT LABEL PAGE
# ======================================================
def create_label_page(stdscr, preset_data=None):
    curses.curs_set(1)

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
        stdscr.addstr(1, 2, title, curses.A_BOLD)
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
        stdscr.addstr(h - 2, 2, "CTRL+N Save | ↑↓ Move | ESC Back")

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
        elif key in (curses.KEY_BACKSPACE, 127):
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


# ======================================================
# SETTINGS
# ======================================================
def settings_page(stdscr):
    curses.curs_set(1)

    old, new, confirm = "", "", ""
    fields = ["old", "new", "confirm"]
    current = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "CHANGE PASSWORD", curses.A_BOLD)

        stdscr.addstr(4, 4, f"Old Password      : {'*' * len(old)}")
        stdscr.addstr(6, 4, f"New Password      : {'*' * len(new)}")
        stdscr.addstr(8, 4, f"Re-enter Password : {'*' * len(confirm)}")

        stdscr.addstr(11, 2, "CTRL+S Save | ESC Back")

        pos = {"old": 4, "new": 6, "confirm": 8}
        val = eval(fields[current])
        stdscr.move(pos[fields[current]], 26 + len(val))
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return None
        elif key == curses.KEY_UP:
            current = (current - 1) % 3
        elif key == curses.KEY_DOWN:
            current = (current + 1) % 3
        elif key == 19:
            if new == confirm and new:
                return True
        elif key in (curses.KEY_BACKSPACE, 127):
            if fields[current] == "old": old = old[:-1]
            elif fields[current] == "new": new = new[:-1]
            elif fields[current] == "confirm": confirm = confirm[:-1]
        elif 32 <= key <= 126:
            if fields[current] == "old": old += chr(key)
            elif fields[current] == "new": new += chr(key)
            elif fields[current] == "confirm": confirm += chr(key)


# ======================================================
# MENU
# ======================================================
def menu_page(stdscr):
    curses.curs_set(0)

    menu = ["Dashboard", "Settings", "Exit"]
    current = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "PYVAULT MENU", curses.A_BOLD)

        for i, m in enumerate(menu):
            if i == current:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + i, 4, m)
            if i == current:
                stdscr.attroff(curses.A_REVERSE)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current = (current - 1) % len(menu)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(menu)
        elif key in (10, 13):
            if menu[current] == "Dashboard":
                dashboard_page(stdscr)
            elif menu[current] == "Settings":
                settings_page(stdscr)
            elif menu[current] == "Exit":
                return
