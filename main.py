import curses
from src.app_controller import AppController

def main(stdscr):
    app = AppController()

    try:
        if not app.db.is_initialized():
            if not app.setup_first_time(stdscr):
                return
        else:
            if not app.verify_master_password(stdscr):
                return
        
        app.run_dashboard(stdscr)

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