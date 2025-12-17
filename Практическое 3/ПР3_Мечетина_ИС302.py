import os

#Генерация файла-ключа (ГПСЧ)
def generate_key_file(filename: str, size: int):
    key = os.urandom(size)
    with open(filename, "wb") as f:
        f.write(key)
    print(f"Ключевой файл создан: {filename}")

#Шифр Вернама (XOR)
def vernam_cipher(input_file: str, key_file: str, output_file: str):
    with open(input_file, "rb") as f:
        data = f.read()

    with open(key_file, "rb") as f:
        key = f.read()

    if len(data) != len(key):
        raise ValueError("Длина ключа должна совпадать с длиной файла")

    result = bytes(d ^ k for d, k in zip(data, key))

    with open(output_file, "wb") as f:
        f.write(result)

    print(f"Файл обработан (Вернам): {output_file}")


#Поточный шифр RC4
def rc4(data: bytes, key: bytes) -> bytes:
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(byte ^ K)

    return bytes(result)


def ПР3_Мечетина_ИС302():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    code_file = os.path.join(base_dir, "code.txt")
    key_file = os.path.join(base_dir, "key.bin")

    if not os.path.exists(code_file):
        print("Ошибка: файл code.txt не найден")
        return

    #Генерация ключа
    size = os.path.getsize(code_file)
    generate_key_file(key_file, size)

    #Шифр Вернама
    vernam_cipher(
        code_file,
        key_file,
        os.path.join(base_dir, "vernam_encrypted.bin")
    )

    vernam_cipher(
        os.path.join(base_dir, "vernam_encrypted.bin"),
        key_file,
        os.path.join(base_dir, "vernam_decrypted.txt")
    )

    #Поточный шифр RC4
    with open(code_file, "rb") as f:
        data = f.read()

    rc4_key = b"secretkey"
    encrypted = rc4(data, rc4_key)

    with open(os.path.join(base_dir, "rc4_encrypted.bin"), "wb") as f:
        f.write(encrypted)

    decrypted = rc4(encrypted, rc4_key)

    with open(os.path.join(base_dir, "rc4_decrypted.txt"), "wb") as f:
        f.write(decrypted)

    print("RC4 шифрование и расшифрование выполнены")
    print("Практическая работа №3 выполнена успешно")

if __name__ == "__main__":
    ПР3_Мечетина_ИС302()
