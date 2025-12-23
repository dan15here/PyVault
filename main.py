import curses

# =============================
# CREATE LABEL PAGE (CTRL+N)
# =============================
def create_label_page(stdscr):
    curses.curs_set(1)

    label = ""
    username = ""
    password = ""
    description = ""

    fields = ["label", "username", "password", "description"]
    current = 0
    show_password = False

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, "CREATE NEW LABEL", curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * 45)

        stdscr.addstr(5, 4, f"Label       : {label}")
        stdscr.addstr(7, 4, f"Username    : {username}")
        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(9, 4, f"Password    : {pwd}")
        stdscr.addstr(11, 4, f"Deskripsi   : {description}")

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(13, 4, f"{checkbox} Show Password (TAB)")

        stdscr.addstr(
            h - 3,
            2,
            "CTRL+N Simpan | TAB Toggle Password | ↑↓ Pindah | ESC Kembali"
        )

        positions = {
            "label": (5, 20 + len(label)),
            "username": (7, 20 + len(username)),
            "password": (9, 20 + len(password)),
            "description": (11, 20 + len(description))
        }

        field = fields[current]
        stdscr.move(*positions[field])

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # ESC
            return None

        elif key == 9:  # TAB
            show_password = not show_password

        elif key == curses.KEY_UP:
            current = (current - 1) % len(fields)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(fields)

        elif key == 14:  # CTRL + N
            if label and username and password:
                return {
                    "label": label,
                    "username": username,
                    "password": password,
                    "description": description
                }

        elif key in (curses.KEY_BACKSPACE, 127):
            if field == "label" and label:
                label = label[:-1]
            elif field == "username" and username:
                username = username[:-1]
            elif field == "password" and password:
                password = password[:-1]
            elif field == "description" and description:
                description = description[:-1]

        elif 32 <= key <= 126:
            if field == "label":
                label += chr(key)
            elif field == "username":
                username += chr(key)
            elif field == "password":
                password += chr(key)
            elif field == "description":
                description += chr(key)


# =============================
# MENU PAGE
# =============================
def menu_page(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    menu = ["Dashboard", "Settings", "Help", "Exit"]
    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(0, 2, "PYVAULT - MAIN MENU")
        stdscr.addstr(1, 2, "-" * 30)
        stdscr.addstr(h - 2, 2, "Shortcut: CTRL+N → Create Label")

        for i, item in enumerate(menu):
            if i == current:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 3, 4, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(i + 3, 4, item)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current = (current - 1) % len(menu)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(menu)

        elif key == 14:  # CTRL + N
            data = create_label_page(stdscr)
            if data:
                stdscr.clear()
                stdscr.addstr(2, 2, "LABEL BERHASIL DIBUAT")
                stdscr.addstr(4, 4, f"Label     : {data['label']}")
                stdscr.addstr(5, 4, f"Username  : {data['username']}")
                stdscr.addstr(6, 4, f"Deskripsi : {data['description']}")
                stdscr.addstr(8, 2, "Tekan tombol apapun...")
                stdscr.getch()

        elif key in (10, 13):
            if menu[current] == "Exit":
                return


# =============================
# LOGIN PAGE
# =============================
def login_page(stdscr):
    curses.curs_set(1)

    h, w = stdscr.getmaxyx()
    bw, bh = 40, 10
    sx = (w - bw) // 2
    sy = (h - bh) // 2

    username = ""
    password = ""
    field = "username"
    show_password = False

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "PYVAULT")

        for i in range(bh):
            stdscr.addstr(sy + i, sx, " " * bw, curses.A_REVERSE)

        welcome = f"Welcome {username}" if username else "Welcome"
        stdscr.addstr(sy + 1, sx + 2, welcome)

        stdscr.addstr(sy + 3, sx + 2, "Username : " + username)
        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(sy + 4, sx + 2, "Password : " + pwd)

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(sy + 6, sx + 2, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(sy + 8, sx + 2, "ENTER Login | ESC Exit")

        if field == "username":
            stdscr.move(sy + 3, sx + 13 + len(username))
        else:
            stdscr.move(sy + 4, sx + 13 + len(password))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:
            return False

        elif key == 9:
            show_password = not show_password

        elif key in (curses.KEY_UP, curses.KEY_DOWN):
            field = "password" if field == "username" else "username"

        elif key in (10, 13):
            if username and password:
                return True

        elif key in (curses.KEY_BACKSPACE, 127):
            if field == "username" and username:
                username = username[:-1]
            elif field == "password" and password:
                password = password[:-1]

        elif 32 <= key <= 126:
            if field == "username":
                username += chr(key)
            else:
                password += chr(key)


# =============================
# MAIN
# =============================
def main(stdscr):
    if login_page(stdscr):
        menu_page(stdscr)

curses.wrapper(main)
