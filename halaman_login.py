import curses

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    box_width = 40
    box_height = 10
    start_x = (width - box_width) // 2
    start_y = (height - box_height) // 2

    username = ""
    password = ""
    show_password = False
    field = "username"

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "PYVAULT")

        # Kotak login
        for i in range(box_height):
            stdscr.addstr(start_y + i, start_x, " " * box_width)

        welcome_text = f"Welcome {username}" if username else "Welcome"
        stdscr.addstr(start_y + 1, start_x + 2, welcome_text)

        stdscr.addstr(start_y + 3, start_x + 2, "Username : " + username)
        pwd_display = password if show_password else "*" * len(password)
        stdscr.addstr(start_y + 4, start_x + 2, "Password : " + pwd_display)

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(start_y + 6, start_x + 2, f"{checkbox} Show Password (TAB)")

        stdscr.addstr(start_y + 8, start_x + 2, "ENTER untuk Login | ESC keluar")

        # Posisi kursor
        if field == "username":
            stdscr.move(start_y + 3, start_x + 13 + len(username))
        else:
            stdscr.move(start_y + 4, start_x + 13 + len(password))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # ESC
            break

        elif key == 9:  # TAB
            show_password = not show_password

        elif key in [10, 13]:  # ENTER
            break

        elif key == curses.KEY_BACKSPACE or key == 127:
            if field == "username" and username:
                username = username[:-1]
            elif field == "password" and password:
                password = password[:-1]

        elif key == curses.KEY_DOWN or key == curses.KEY_UP:
            field = "password" if field == "username" else "username"

        elif 32 <= key <= 126:
            if field == "username":
                username += chr(key)
            else:
                password += chr(key)

    # Hasil akhir
    stdscr.clear()
    stdscr.addstr(height // 2, (width // 2) - 10, f"Login sebagai {username}")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
