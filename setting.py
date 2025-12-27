import curses

def settings_page(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)

    old_password = ""
    new_password = ""
    confirm_password = ""
    show_password = False

    fields = ["old", "new", "confirm"]
    current = 0
    error_msg = ""

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Header
        stdscr.addstr(1, 2, "SETTINGS", curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * 40)
        stdscr.addstr(3, 2, "Change Password", curses.A_BOLD)

        # Password display
        def mask(pwd):
            return pwd if show_password else "*" * len(pwd)

        stdscr.addstr(6, 4, f"Old Password      : {mask(old_password)}")
        stdscr.addstr(8, 4, f"New Password      : {mask(new_password)}")
        stdscr.addstr(10, 4, f"Re-enter Password : {mask(confirm_password)}")

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(12, 4, f"{checkbox} Show Password (TAB)")

        # Error message
        if error_msg:
            stdscr.addstr(14, 4, error_msg, curses.A_BOLD | curses.A_REVERSE)

        stdscr.addstr(
            h - 3,
            2,
            "CTRL+S Simpan | TAB Toggle | ↑↓ Pindah | ESC Kembali"
        )

        # Cursor positions
        positions = {
            "old": (6, 26 + len(old_password)),
            "new": (8, 26 + len(new_password)),
            "confirm": (10, 26 + len(confirm_password))
        }

        stdscr.move(*positions[fields[current]])
        stdscr.refresh()

        key = stdscr.getch()
        field = fields[current]

        # ESC
        if key == 27:
            return None

        # TAB
        elif key == 9:
            show_password = not show_password

        # NAVIGASI
        elif key == curses.KEY_UP:
            current = (current - 1) % len(fields)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(fields)

        # SIMPAN (CTRL+S)
        elif key == 19:
            if not old_password or not new_password or not confirm_password:
                error_msg = "Semua field wajib diisi"
            elif new_password != confirm_password:
                error_msg = "Password baru tidak cocok"
            else:
                return {
                    "old_password": old_password,
                    "new_password": new_password
                }

        # BACKSPACE
        elif key in (curses.KEY_BACKSPACE, 127):
            if field == "old":
                old_password = old_password[:-1]
            elif field == "new":
                new_password = new_password[:-1]
            elif field == "confirm":
                confirm_password = confirm_password[:-1]

        # INPUT
        elif 32 <= key <= 126:
            if field == "old":
                old_password += chr(key)
            elif field == "new":
                new_password += chr(key)
            elif field == "confirm":
                confirm_password += chr(key)
