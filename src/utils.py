import time
import pyperclip
import threading


try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("[Warning] pyperclip not installed. Clipboard feature disabled.")
    print("Install with: pip install pyperclip")

def _wipe_clipboard(delay):
    if CLIPBOARD_AVAILABLE:
        try:
            time.sleep(delay) 
            pyperclip.copy("") 
        except:
            pass

def copy_to_clipboard(text, auto_clear=True, clear_delay=15):
    if not CLIPBOARD_AVAILABLE:
        return

    try:
        pyperclip.copy(text)

        if auto_clear:
            t = threading.Thread(
                target=_wipe_clipboard, 
                args=(clear_delay,),
                daemon=True 
                )
            t.start()
        return True

    except Exception as e:
        print(f"[Error] Failed to copy to clipboard: {e}")
        return False
    
def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letetr"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain number"
    return True, "Strong password"

