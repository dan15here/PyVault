import curses

labels = [
    "Label 1: File",
    "Label 2: Edit",
    "Label 3: View",
    "Label 4: Help",
    "Label 5: Exit"
]

def main(stdscr):
    curses.curs_set(0)  # sembunyikan cursor
    stdscr.keypad(True)

    current = 0
    selected = [False] * len(labels)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Header
        stdscr.addstr(0, 2, "Multi Select (Arrow ↑↓ | SPACE select | ENTER confirm)")

        # Render label
        for i, label in enumerate(labels):
            marker = "[x]" if selected[i] else "[ ]"

            if i == current:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 2, 4, f"{marker} {label}")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 4, f"{marker} {label}")

        # Status bar
        stdscr.addstr(h - 1, 2, "CTRL+C Exit")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current = (current - 1) % len(labels)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(labels)
        elif key == ord(" "):
            selected[current] = not selected[current]
        elif key in (curses.KEY_ENTER, 10, 13):
            break

    # Hasil akhir
    stdscr.clear()
    stdscr.addstr(1, 2, "Label terpilih:")
    row = 3
    for i, val in enumerate(selected):
        if val:
            stdscr.addstr(row, 4, labels[i])
            row += 1

    stdscr.addstr(row + 1, 2, "Tekan tombol apapun untuk keluar...")
    stdscr.getch()

curses.wrapper(main)
