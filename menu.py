import curses
from dashboard import dashboard_page
from setting import settings_page


def menu_page(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    menu = ["Dashboard", "Settings", "Exit"]
    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Header
        stdscr.addstr(0, 2, "PYVAULT - MAIN MENU", curses.A_BOLD)
        stdscr.addstr(1, 2, "-" * 30)
        stdscr.addstr(h - 2, 2, "ENTER Select | ↑↓ Navigate")

        # Menu
        for i, item in enumerate(menu):
            y = 3 + i
            if i == current:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, 4, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, 4, item)

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
                result = settings_page(stdscr)
                if result:
                    stdscr.clear()
                    stdscr.addstr(2, 2, "PASSWORD BERHASIL DIUBAH", curses.A_BOLD)
                    stdscr.addstr(4, 2, "Tekan tombol apapun...")
                    stdscr.getch()

            elif menu[current] == "Exit":
                return
