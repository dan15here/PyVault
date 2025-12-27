import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoManager:
    def __init__(self):
        # Konfigurasi Argon2 sesuai standar keamanan
        self.time_cost = 2
        self.memory_cost = 65536 # 64MB
        self.parallelism = 2
        self.hash_len = 32

    def generate_salt(self):
        """
        Membuat data acak 16 byte sebagai bumbu (salt)
        Salt digunakan untuk mencegah rainbow table attacks.
        """
        return os.urandom(16)

    def derive_key(self, master_password, salt):
        """
        Mengubah Password -> Key 32-byte (AES-256) menggunakan Argon2id.
        Berbasis memory-hard sehingga tahan serangan bruteforce menggunakan GPU.
        """
        return hash_secret_raw(
            secret=master_password.encode(),
            salt=salt,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=32,
            type=Type.ID   # Argon2id (hybrid mode)
        )

    def hash_verifier(self, key, salt):
        """
        Membuat hash dari encryption key untuk disimpan di DB (Verifier).
        Digunakan untuk login check tanpa menyimpan key asli.
        """
        return hash_secret_raw(
            secret=key,
            salt=salt,
            time_cost=1,
            memory_cost=1024,
            parallelism=1,
            hash_len=32,
            type=Type.ID
        )

    def encrypt_data(self, key, plaintext):
        """
        Mengunci data menggunakan AES-256-GCM.
        Args: (key, plaintext)
        Return: (ciphertext, nonce)
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(12) # GCM standard 12-byte nonce
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return ciphertext, nonce

    def decrypt_data(self, key, ciphertext, nonce):
        """
        Dekripsi data menggunakan AES-256-GCM.
        Args: (key, ciphertext, nonce)
        Returns: plaintext
        """
        try:
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode()
        except Exception as e:
            raise ValueError("Dekripsi gagal: kunci salah atau data corrupt") from e