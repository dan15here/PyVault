import time
import pyperclip
import threading

def _wipe_clipboard(delay):
    """ Fungsi rahasia yang berjalan di background"""
    time.sleep(delay)
    pyperclip.copy("") # Hapus clipboard demi keamanan

def copy_to_clipboard(text):
    """
    Menyalin teks dan menyuruh 'asisten' (thread) 
    untuk mmenghapusnya nanti, jadi aplikasi utama tidak macet.    
    """
    try:
        pyperclip.copy(text)
        # Jalankan penghapusan di jalur terpisah (background thread)
        t = threading.Thread(target=_wipe_clipboard, args=(15,))
        t.start()
    except Exception:
        pass