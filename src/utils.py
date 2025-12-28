import time
import pyperclip
import threading

def _wipe_clipboard(delay):
    time.sleep(delay)
    pyperclip.copy("") # Hapus clipboard demi keamanan

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        # Jalankan penghapusan di jalur terpisah (background thread)
        t = threading.Thread(target=_wipe_clipboard, args=(15,))
        t.start()
    except Exception:
        pass