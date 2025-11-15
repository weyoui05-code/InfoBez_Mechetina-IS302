import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import math

#Константы алфавитов
RUSSIAN_LOWER = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUSSIAN_UPPER = RUSSIAN_LOWER.upper()
LATIN_LOWER = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
LATIN_UPPER = LATIN_LOWER.upper()
DIGITS = '0123456789'

#формирование итогового алфавита по выбранным параметрам.
def build_alphabet(use_latin, use_russian, use_digits, case_sensitive, special_symbols_text):
    """
    Возвращает итоговый алфавит (строка уникальных символов) в соответствии с опциями.
    """
    parts = []
    if use_latin:
        parts.append(LATIN_LOWER)
        if case_sensitive:
            parts.append(LATIN_UPPER)
    if use_russian:
        parts.append(RUSSIAN_LOWER)
        if case_sensitive:
            parts.append(RUSSIAN_UPPER)
    if use_digits:
        parts.append(DIGITS)
    # Спецсимволы добавляем как есть (пользователь вводит)
    if special_symbols_text:
        parts.append(special_symbols_text)
    # Объединим и удалим дубли, сохраняя порядок первого появления
    joined = ''.join(parts)
    seen = set()
    uniq = []
    for ch in joined:
        if ch not in seen:
            seen.add(ch)
            uniq.append(ch)
    return ''.join(uniq)

#вычисление количества возможных комбинаций.
def count_passwords(alphabet_size, password_length):
    """
    Количество всех возможных паролей: alphabet_size ** password_length.
    Возвращаем int (могут быть очень большие числа).
    """
    if alphabet_size <= 0 or password_length <= 0:
        return 0
    return pow(alphabet_size, password_length)

#красивое отображение больших чисел
def nice_number(n):
    try:
        s_exact = str(n)
        if n == 0:
            return "0"
        exp = "{:.3e}".format(n)
        return f"{s_exact}  ({exp})"
    except Exception:
        return str(n)


#проверка пересечения спецсимволов.
def validate_special_symbols(special, use_latin, use_russian, use_digits, case_sensitive):
    """
    Проверяем, чтобы спецсимволы не пересекались с выбранными наборами.
    Возвращаем (ok: bool, message: str).
    Заметь: если case_sensitive True, то проверяем и большие буквы; иначе — только нижний регистр.
    """
    conflicts = []
    check_set = set()
    if use_latin:
        check_set.update(LATIN_LOWER)
        if case_sensitive:
            check_set.update(LATIN_UPPER)
    if use_russian:
        check_set.update(RUSSIAN_LOWER)
        if case_sensitive:
            check_set.update(RUSSIAN_UPPER)
    if use_digits:
        check_set.update(DIGITS)
    for ch in special:
        if ch in check_set:
            conflicts.append(ch)
    if conflicts:
        return False, f"Введённые спецсимволы содержат символы из выбранных наборов: {', '.join(sorted(set(conflicts)))}"
    return True, ""


#основной класс приложения
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Генератор паролей — подсчёт количества комбинаций")
        frame = ttk.Frame(root, padding=12)
        frame.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        params = ttk.LabelFrame(frame, text="Параметры генерации пароля", padding=10)
        params.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        params.columnconfigure(1, weight=1)

        # Длина пароля
        ttk.Label(params, text="Длина пароля (1..64):").grid(row=0, column=0, sticky="w")
        self.length_var = tk.StringVar(value="8")
        self.length_entry = ttk.Entry(params, textvariable=self.length_var, width=8)
        self.length_entry.grid(row=0, column=1, sticky="w", padx=4)

        self.use_latin_var = tk.BooleanVar(value=True)
        self.use_russian_var = tk.BooleanVar(value=False)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.case_sensitive_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(params, text="Использовать строчные латинские буквы", variable=self.use_latin_var).grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(params, text="Использовать строчные русские буквы", variable=self.use_russian_var).grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(params, text="Использовать цифры", variable=self.use_digits_var).grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(params, text="Учитывать регистр (разрешить заглавные буквы)", variable=self.case_sensitive_var).grid(row=4, column=0, columnspan=2, sticky="w")

        ttk.Label(params, text="Спецсимволы (введите перечень):").grid(row=5, column=0, sticky="w", pady=(6,0))
        self.special_text = tk.Text(params, height=2, width=40)
        self.special_text.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0,6))

        buttons_frame = ttk.Frame(params)
        buttons_frame.grid(row=7, column=0, columnspan=2, sticky="ew")
        self.compute_btn = ttk.Button(buttons_frame, text="Вычислить и сгенерировать пароль", command=self.on_compute)
        self.compute_btn.grid(row=0, column=0, padx=2, pady=4)
        self.copy_btn = ttk.Button(buttons_frame, text="Копировать пароль", command=self.copy_password)
        self.copy_btn.grid(row=0, column=1, padx=2, pady=4)

        #Нижняя часть: результаты
        results = ttk.LabelFrame(frame, text="Результаты", padding=10)
        results.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        results.columnconfigure(1, weight=1)

        ttk.Label(results, text="Итоговый алфавит:").grid(row=0, column=0, sticky="nw")
        self.alphabet_display = tk.Text(results, height=2, width=60, state="disabled")
        self.alphabet_display.grid(row=0, column=1, sticky="ew", padx=4, pady=2)

        ttk.Label(results, text="Размер алфавита (кол-во символов):").grid(row=1, column=0, sticky="w")
        self.alphabet_size_var = tk.StringVar(value="0")
        ttk.Label(results, textvariable=self.alphabet_size_var).grid(row=1, column=1, sticky="w")

        ttk.Label(results, text="Количество возможных паролей:").grid(row=2, column=0, sticky="w")
        self.count_var = tk.StringVar(value="0")
        ttk.Label(results, textvariable=self.count_var).grid(row=2, column=1, sticky="w")

        ttk.Label(results, text="Сгенерированный пароль:").grid(row=3, column=0, sticky="w", pady=(6,0))
        self.generated_var = tk.StringVar(value="")
        ttk.Entry(results, textvariable=self.generated_var, font=("TkDefaultFont", 12), width=40).grid(row=3, column=1, sticky="w", pady=(6,0))

        # Проверка: кнопка проверки введённого пароля на соответствие требованиям (доп.функция)
        self.check_entry = ttk.Entry(results, width=40)
        self.check_entry.grid(row=4, column=1, sticky="w", pady=(6,0))
        ttk.Button(results, text="Проверить введённый пароль на соответствие требованиям", command=self.check_user_password).grid(row=4, column=0, sticky="w", padx=2, pady=(6,0))

        # Установки по умолчанию: показать подсказку в спецсимволах
        self.special_text.insert("1.0", "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'")

        self.on_compute()

    def on_compute(self):
        # Валидация длины
        length_str = self.length_var.get().strip()
        try:
            length = int(length_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Длина пароля должна быть целым числом.")
            return
        if length < 1 or length > 64:
            messagebox.showerror("Ошибка", "Длина пароля должна быть в диапазоне от 1 до 64.")
            return

        use_latin = self.use_latin_var.get()
        use_russian = self.use_russian_var.get()
        use_digits = self.use_digits_var.get()
        case_sensitive = self.case_sensitive_var.get()
        special = self.special_text.get("1.0", "end").strip()

        # Проверка пересечения спецсимволов с выбранными наборами
        ok, msg = validate_special_symbols(special, use_latin, use_russian, use_digits, case_sensitive)
        if not ok:
            messagebox.showerror("Ошибка в спецсимволах", msg)
            return

        alphabet = build_alphabet(use_latin, use_russian, use_digits, case_sensitive, special)
        alphabet_size = len(alphabet)

        if alphabet_size == 0:
            messagebox.showerror("Ошибка", "Итоговый алфавит пуст. Выберите хотя бы один набор символов или введите спецсимволы.")
            return

        # Количество паролей
        total = count_passwords(alphabet_size, length)

        # Результат: показать алфавит и число
        self.alphabet_display.configure(state="normal")
        self.alphabet_display.delete("1.0", "end")
        self.alphabet_display.insert("1.0", alphabet)
        self.alphabet_display.configure(state="disabled")

        self.alphabet_size_var.set(str(alphabet_size))
        self.count_var.set(nice_number(total))

        # Сгенерировать случайный пароль
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        self.generated_var.set(password)

    def copy_password(self):
        pwd = self.generated_var.get()
        if not pwd:
            messagebox.showinfo("Копирование", "Пароль пустой — сначала сгенерируйте пароль.")
            return
        # Копирование в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        messagebox.showinfo("Копирование", "Пароль скопирован в буфер обмена.")

    def check_user_password(self):
        """
        Доп.функция: проверяет введённый пользователем пароль (в поле под результатом)
        на соответствие текущим требованиям (наличие символов из итогового алфавита,
        длина, и если заданы обязательные требования — тут базовая проверка).
        """
        pwd = self.check_entry.get()
        if not pwd:
            messagebox.showinfo("Проверка", "Введите пароль для проверки в поле ввода.")
            return

        # Получим текущие настройки и алфавит
        use_latin = self.use_latin_var.get()
        use_russian = self.use_russian_var.get()
        use_digits = self.use_digits_var.get()
        case_sensitive = self.case_sensitive_var.get()
        special = self.special_text.get("1.0", "end").strip()
        alphabet = build_alphabet(use_latin, use_russian, use_digits, case_sensitive, special)
        length_str = self.length_var.get().strip()
        try:
            required_len = int(length_str)
        except ValueError:
            required_len = None

        problems = []
        if required_len is not None and len(pwd) != required_len:
            problems.append(f"Длина пароля должна быть {required_len}, а введено {len(pwd)}.")
        # символы не из алфавита
        bad_chars = sorted(set(ch for ch in pwd if ch not in alphabet))
        if bad_chars:
            problems.append(f"Пароль содержит символы, не входящие в итоговый алфавит: {', '.join(bad_chars)}")
        if problems:
            messagebox.showwarning("Проверка пароля — обнаружены проблемы", "\n".join(problems))
        else:
            messagebox.showinfo("Проверка пароля", "Пароль соответствует текущим требованиям.")

# ---------- Запуск приложения ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
