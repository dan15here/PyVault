import curses

def login_page(stdscr):
    curses.curs_set(1)

    h, w = stdscr.getmaxyx()
    bw, bh = 40, 9
    sx = (w - bw) // 2
    sy = (h - bh) // 2

    password = ""
    show_password = False

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "PYVAULT")

        for i in range(bh):
            stdscr.addstr(sy + i, sx, " " * bw)

        stdscr.addstr(sy + 2, sx + 2, "LOGIN")

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(sy + 4, sx + 2, "Password : " + pwd)

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(sy + 6, sx + 2, f"{checkbox} Show Password (TAB)")
        stdscr.addstr(sy + 7, sx + 2, "ENTER Login | ESC Exit")

        stdscr.move(sy + 4, sx + 13 + len(password))
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
