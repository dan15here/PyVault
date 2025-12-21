import time
import pyperclip
from src import utils

def run_test():
    print("=== PENGUJIAN FILE UTILS.PY ===")
    
    # 1. Siapkan data rahasia palsu
    rahasia = "Inipasswordjanganbuka"
    print(f"\n[Langkah 1] Mencoba menyalin teks: '{rahasia}'")
    
    # 2. Panggil fungsi dari utils.py
    # Ini harusnya menyalin teks, lalu membuat thread background yang menunggu 15 detik
    utils.copy_to_clipboard(rahasia)
    
    # Beri jeda sedikit agar komputer sempat memproses perintah copy
    time.sleep(1)
    
    # 3. Cek apakah clipboard sudah terisi (Verifikasi Copy)
    isi_clipboard_sekarang = pyperclip.paste()
    if isi_clipboard_sekarang == rahasia:
        print("   [SUKSES] Clipboard berhasil diisi!")
    else:
        print(f"   [GAGAL] Clipboard isinya malah: '{isi_clipboard_sekarang}'")
        print("   (Pastikan 'xclip' sudah terinstall: sudo apt install xclip)")
        return # Berhenti jika copy saja gagal

    # 4. Tunggu 15 detik untuk mengetes Wiper (Verifikasi Threading)
    print("\n[Langkah 2] Menunggu 16 detik untuk melihat apakah clipboard dihapus...")
    print("   (Program tidak boleh macet/freeze di sini karena pakai Threading)")
    
    for i in range(16, 0, -1):
        print(f"   Sisa waktu: {i} detik...   ", end='\r')
        time.sleep(1)
    
    print("\n   Waktu habis! Memeriksa clipboard...")

    # 5. Cek apakah clipboard sudah kosong (Verifikasi Wiper)
    isi_akhir = pyperclip.paste()
    
    if isi_akhir == "":
        print("\n[SUKSES] Clipboard KOSONG. Fitur keamanan berfungsi!")
    else:
        print(f"\n[GAGAL] Clipboard masih berisi: '{isi_akhir}'")

if __name__ == "__main__":
    run_test()