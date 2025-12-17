from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

def aes_encrypt(input_file, output_file, key):
    with open(input_file, "rb") as f:
        data = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    with open(output_file, "wb") as f:
        f.write(cipher.iv)
        f.write(ciphertext)

    print(f"Файл зашифрован: {output_file}")

def aes_decrypt(input_file, output_file, key):
    with open(input_file, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"Файл расшифрован: {output_file}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plaintext = os.path.join(base_dir, "code.txt")
    encrypted = os.path.join(base_dir, "aes_encrypted.bin")
    decrypted = os.path.join(base_dir, "aes_decrypted.txt")
    if not os.path.exists(plaintext):
        print("Ошибка: файл code.txt не найден")
        return
    # Ключ AES (128 бит)
    key = get_random_bytes(16)
    # Шифрование
    aes_encrypt(plaintext, encrypted, key)
    # Расшифрование
    aes_decrypt(encrypted, decrypted, key)

    print("Практическая работа №4 выполнена успешно")
if __name__ == "__main__":
    main()
