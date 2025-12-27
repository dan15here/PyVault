import curses
from create_label import create_label_page


def dashboard_page(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    # ===== DUMMY DATA =====
    items = [
        {
            "label": "akun steam",
            "site": "www.steam.com",
            "username": "GodOfHyperdeath",
            "password": "chara1234",
            "description": "Akun utama steam"
        },
        {
            "label": "akun steam 2",
            "site": "www.steam.com",
            "username": "AltAccount",
            "password": "password123",
            "description": "Akun cadangan"
        }
    ]

    current = 0
    message = ""

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(0, 2, "DASHBOARD", curses.A_BOLD)
        stdscr.addstr(1, 2, "-" * 40)

        y = 3
        for i, item in enumerate(items):
            if y + 5 >= h:
                break

            if i == current:
                stdscr.attron(curses.A_REVERSE)

            stdscr.addstr(y, 4, f"Label    : {item['label']}")
            stdscr.addstr(y + 1, 4, f"Site     : {item['site']}")
            stdscr.addstr(y + 2, 4, f"Username : {item['username']}")
            stdscr.addstr(y + 3, 4, f"Password : {'*' * len(item['password'])}")

            if i == current:
                stdscr.attroff(curses.A_REVERSE)

            y += 6

        stdscr.addstr(
            h - 3,
            2,
            "↑↓ Pilih | CTRL+N New | E Edit | O Copy | ESC Back"
        )

        if message:
            stdscr.addstr(h - 2, 2, message)

        stdscr.refresh()
        key = stdscr.getch()
        message = ""

        # ===== INPUT =====
        if key == curses.KEY_UP:
            current = (current - 1) % len(items)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(items)

        elif key == 14:  # CTRL+N CREATE
            new_item = create_label_page(stdscr)
            if new_item:
                items.append(new_item)
                current = len(items) - 1
                message = "Label baru ditambahkan"

        elif key in (ord("e"), ord("E")):  # EDIT
            edited = create_label_page(stdscr, preset_data=items[current])
            if edited:
                items[current] = edited
                message = "Label berhasil diubah"

        elif key in (ord("o"), ord("O")):  # COPY
            message = f"Password '{items[current]['password']}' disalin"

        elif key == 27:  # ESC
            return
