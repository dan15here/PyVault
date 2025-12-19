import os 
import base64
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
    def __init__(self):
        # Inisialisasi Argon2 (Untuk Hashing Master Password)
        self.ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)
    
    def generate_salt(self):
        """Membuat data acak 16 byte sebagai bumbu (salt)"""
        return os.urandom(16) # 16 Bytes (128 bit) data acak. Ini adalah standar industri

    def hash_master_password(self, password):
        """
        Mengubah Master Password menjadi Hash (Pake Argon2).
        Output: String Hash yang aman disimpan di DataBase.
        """
        return self.ph.hash(password)
    
    def verify_master_password(self, stored_hash, input_password):
        try:
            self.ph.verify(stored_hash, input_password)
            return True
        except VerifyMismatchError:
            return False
    
    def derive_encryption_key(self, master_password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def encrypt_data(self, key, plaintext):
        """Mengunci data. Input: Teks biasa ===> Output: Teks acak (bytes)"""
        f = Fernet(key)
        return f.encrypt(plaintext.encode())
    
    def decrypt_data(self, key, plaintext):
        """Membuka data. Input: Teks acak ===> Output: Teks biasa (string)"""
        f = Fernet(key)
        return f.decrypt(plaintext).decode()
    
# ==========================================
# AREA PENGUJIAN (TESTING AREA)
# Kode di bawah ini hanya jalan kalau file ini dijalankan langsung
# ==========================================
if __name__ == "__main__":
    print("--- MULAI TEST SECURITY ---")
    
    # 1. Bikin Objek Security
    crypto = CryptoManager()
    
    # 2. Skenario: User Baru Daftar
    password_user = "Danish123"
    print(f"\n[1] Password Asli User: {password_user}")
    
    # Test Hashing (Untuk Login)
    hash_di_db = crypto.hash_master_password(password_user)
    print(f"[1] Hash tersimpan: {hash_di_db}... (dipotong biar gak kepanjangan)")
    
    # 3. Skenario: User Coba Login
    print("\n[2] Testing Login...")
    
    # Coba login pakai password BENAR
    cek_benar = crypto.verify_master_password(hash_di_db, "Danish123")
    print(f"    - Login pakai 'Danish123': {'BERHASIL ✅' if cek_benar else 'GAGAL ❌'}")
    
    # Coba login pakai password SALAH
    cek_salah = crypto.verify_master_password(hash_di_db, "Anjing123")
    print(f"    - Login pakai 'Anjing123': {'BERHASIL ❌' if cek_salah else 'GAGAL (Aman) ✅'}")

    # 4. Skenario: Enkripsi Data
    print("\n[3] Testing Enkripsi Data...")
    
    # Kita butuh salt dan kunci dulu
    salt_dummy = crypto.generate_salt()
    key = crypto.derive_encryption_key(password_user, salt_dummy)
    print(f"    - Key Enkripsi (Base64): {key.decode()}")
    
    # Data rahasia yang mau diamankan
    rahasia = "PasswordFacebookGue"
    print(f"    - Plaintext: {rahasia}")
    
    # Kunci datanya
    encrypted = crypto.encrypt_data(key, rahasia)
    print(f"    - Ciphertext (Terenkripsi): {encrypted}")
    
    # Buka lagi datanya
    decrypted = crypto.decrypt_data(key, encrypted)
    print(f"    - Hasil Dekripsi: {decrypted}")
    
    # Verifikasi Akhir
    if rahasia == decrypted:
        print("\nKESIMPULAN: ✅ SEMUA FUNGSI BERJALAN NORMAL!")
    else:
        print("\nKESIMPULAN: ❌ ADA YANG ERROR!")