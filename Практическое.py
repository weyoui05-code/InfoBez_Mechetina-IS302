import sys
from collections import Counter
from pathlib import Path
import math

def read_text_file_guess_encoding(path: Path) -> str:
    """Пробуем читать как UTF-8, иначе fallback на latin-1."""
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return path.read_text(encoding='latin-1')

def format_char_display(ch: str) -> str:
    if ch == ' ':
        return "' ' (SPACE)"
    if ch == '\n':
        return "'\\n' (LF)"
    if ch == '\r':
        return "'\\r' (CR)"
    if ch == '\t':
        return "'\\t' (TAB)"
    if ch.isprintable():
        return f"'{ch}'"
    return f"U+{ord(ch):04X}"

def count_char_frequencies(text: str) -> Counter:
    """Возвращает Counter с частотами символов в тексте."""
    return Counter(text)

def compute_entropy(counter: Counter, total: int) -> float:
    """
    Вычисляет энтропию Шеннона в битах на символ:
    H = - sum_{i} p_i * log2(p_i), где p_i = count_i / total.
    Возвращает H (float). Если total == 0 -> возвращает 0.0.
    """
    if total == 0:
        return 0.0
    H = 0.0
    for cnt in counter.values():
        p = cnt / total
        if p > 0.0:
            H -= p * math.log2(p)
    return H

def print_frequencies_and_entropy(counter: Counter, total: int, top_n: int = None) -> None:
    """Печатает таблицу частот и результаты по энтропии."""
    items = counter.most_common(top_n)
    print(f"Всего символов: {total}")
    print(f"{'№':>3} | {'Символ':^15} | {'Количество':^8} | {'Процент':^8}")
    print("-" * 45)
    for i, (ch, cnt) in enumerate(items, start=1):
        display = format_char_display(ch)
        percent = cnt / total * 100 if total > 0 else 0.0
        print(f"{i:3d} | {display:^15} | {cnt:8d} | {percent:7.3f}%")
    print("-" * 45)

    # Энтропию
    H = compute_entropy(counter, total)
    total_bits = H * total
    print(f"\nЭнтропия (Шеннона): H = {H:.6f} бит/символ")
    print(f"Общая энтропия:     H * N = {total_bits:.3f} бит")

def main():
    # Путь к файлу
    if len(sys.argv) >= 2:
        file_path = Path(sys.argv[1])
    else:
        file_path = Path(input("Введите путь к файлу: ").strip())

    if not file_path.exists():
        print(f"Ошибка: файл не найден: {file_path}")
        return

    # Читаем файл
    try:
        text = read_text_file_guess_encoding(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    freq = count_char_frequencies(text)
    total_chars = sum(freq.values())

    top_n = None
    print(f"\nФайл: {file_path}\n")
    print_frequencies_and_entropy(freq, total_chars, top_n=top_n)

if __name__ == "__main__":
    main()
