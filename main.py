import curses
from login import login_page
from menu import menu_page

def main(stdscr):
    if login_page(stdscr):
        menu_page(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)