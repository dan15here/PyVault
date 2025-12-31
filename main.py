import curses
from src.app_controller import AppController
from src.logger import get_logger

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # Header
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # Success
    curses.init_pair(3, curses.COLOR_RED, -1)      # Error
    curses.init_pair(4, curses.COLOR_YELLOW, -1)   # Highlight

def main(stdscr):
    init_colors()
    logger = get_logger()
    logger.log_app_start()
    app = AppController()

    try:
        if not app.db.is_initialized():
            if not app.setup_first_time(stdscr):
                return
        else:
            if not app.verify_master_password(stdscr):
                return
        
        app.run_main_menu(stdscr)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        stdscr.clear()
        stdscr.addstr(1, 1, "ERROR OCCURED:", curses.A_BOLD)
        stdscr.addstr(3, 1, str(e))
        stdscr.addstr(5, 1, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()

    finally:
         app.close()

if __name__ == "__main__":
    curses.wrapper(main)