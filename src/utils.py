import time
import threading
import secrets
import string


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
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in symbols for c in password):
        return False
    return True

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    if length < 8:
        length = 8
    
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    punctuation = string.punctuation
    
    char_pool = ""
    required_chars = []
    
    if use_uppercase:
        char_pool += uppercase
        required_chars.append(secrets.choice(uppercase))
    if use_lowercase:
        char_pool += lowercase
        required_chars.append(secrets.choice(lowercase))
    if use_digits:
        char_pool += digits
        required_chars.append(secrets.choice(digits))
    if use_symbols:
        char_pool += punctuation
        required_chars.append(secrets.choice(punctuation))
    
    if not char_pool:
        char_pool = lowercase + digits
        required_chars = [secrets.choice(lowercase), secrets.choice(digits)]
    
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)
