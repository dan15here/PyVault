import curses


def create_label_page(stdscr, preset_data=None):
    curses.curs_set(1)
    stdscr.keypad(True)

    # ===== INIT DATA (CREATE / EDIT MODE) =====
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

        title = "EDIT LABEL" if preset_data else "CREATE NEW LABEL"
        stdscr.addstr(1, 2, title, curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * min(45, w - 4))

        stdscr.addstr(5, 4, f"Label       : {label}")
        stdscr.addstr(7, 4, f"Site        : {site}")
        stdscr.addstr(9, 4, f"Username    : {username}")

        pwd = password if show_password else "*" * len(password)
        stdscr.addstr(11, 4, f"Password    : {pwd}")

        # Deskripsi multiline
        stdscr.addstr(13, 4, "Deskripsi   :")
        lines = description.split("\n") if description else [""]

        for i, line in enumerate(lines[:3]):
            if 14 + i < h - 6:
                stdscr.addstr(14 + i, 18, line[: w - 20])

        checkbox = "[x]" if show_password else "[ ]"
        stdscr.addstr(h - 5, 4, f"{checkbox} Show Password (TAB)")

        stdscr.addstr(
            h - 3,
            2,
            "CTRL+N Simpan | TAB Toggle | ↑↓ Pindah | ENTER Baris Baru | ESC Kembali"
        )

        # ===== CURSOR POSITION (AMAN) =====
        field = fields[current]
        if field == "description":
            y = min(14 + len(lines) - 1, h - 6)
            x = min(18 + len(lines[-1]), w - 2)
        else:
            y_map = {"label": 5, "site": 7, "username": 9, "password": 11}
            value = eval(field)
            y = y_map[field]
            x = min(20 + len(value), w - 2)

        stdscr.move(y, x)
        stdscr.refresh()

        key = stdscr.getch()

        # ===== INPUT HANDLING =====
        if key == 27:  # ESC
            return None

        elif key == 9:  # TAB
            show_password = not show_password

        elif key == curses.KEY_UP:
            current = (current - 1) % len(fields)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(fields)

        elif key == 14:  # CTRL+N SAVE
            if label and site and username and password:
                return {
                    "label": label,
                    "site": site,
                    "username": username,
                    "password": password,
                    "description": description
                }

        elif key in (curses.KEY_BACKSPACE, 127):
            if field == "label":
                label = label[:-1]
            elif field == "site":
                site = site[:-1]
            elif field == "username":
                username = username[:-1]
            elif field == "password":
                password = password[:-1]
            elif field == "description":
                description = description[:-1]

        elif key in (10, 13):  # ENTER
            if field == "description":
                description += "\n"

        elif 32 <= key <= 126:
            if field == "label":
                label += chr(key)
            elif field == "site":
                site += chr(key)
            elif field == "username":
                username += chr(key)
            elif field == "password":
                password += chr(key)
            elif field == "description":
                description += chr(key)
