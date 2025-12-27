import curses
from src.tui import menu_page, login_page


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    if login_page(stdscr):
        menu_page(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
