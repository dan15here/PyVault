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
        return os.urandom(16)

    def derive_key(self, master_password, salt):
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
        # 1. Initialize AES-GCM
        aesgcm = AESGCM(key)
        # 2. Generate unique 12-byte Nonce (Number used Once)
        nonce = os.urandom(12)
         # 3. Encrypt data                                           
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None) 
         # 4. Return combined bytes  
        return ciphertext, nonce                                       

    def decrypt_data(self, key, ciphertext, nonce):
        try:
             # 1. Initialize AES-GCM
            aesgcm = AESGCM(key)
             # 2. Decrypt ciphertext using nonce
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)    
             # 3. Converts raw bytes into a readable string    
            return plaintext.decode()                                 
        except Exception as e:
            raise ValueError("Decryption failed: wrong key or corrupt data") from e