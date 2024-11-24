import tkinter as tk
import configparser
import os
import sys
from datetime import datetime

# Имя файла для хранения настроек
SETTINGS_FILE = 'TopClock.ini'

# Константы для ключей настроек
BG_COLOR = 'bg_color'
FONT_SIZE = 'font_size'
FONT_NAME = 'font_name'
FONT_STYLE = 'font_style'
FONT_COLOR = 'font_color'
POSITION = 'position'
SHOW_SECONDS = 'show_seconds'
WIDTH_INCREASE_PERCENT = 'width_increase_percent'
HEIGHT_INCREASE_PERCENT = 'height_increase_percent'
SECONDS_BAR_COLOR = 'seconds_bar_color'
SECONDS_BAR_HEIGHT = 'seconds_bar_height'

# Функция для загрузки настроек из файла
def load_settings() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    settings_path = get_settings_path()
    if os.path.exists(settings_path):
        config.read(settings_path, encoding='utf-8')
        if not config.has_section('Settings'):
            create_default_settings(settings_path)
            config.read(settings_path, encoding='utf-8')
    else:
        create_default_settings(settings_path)
        config.read(settings_path, encoding='utf-8')
    return config

# Функция для создания файла настроек по умолчанию
def create_default_settings(settings_path: str) -> None:
    settings_content = """
[Settings]
; Цвет фона окна
bg_color = #1E1E1E

; Размер шрифта
font_size = 48

; Название шрифта
font_name = Tahoma

; Стиль шрифта (normal, bold, italic)
font_style = bold

; Цвет шрифта
font_color = #D4D4D4

; Положение окна (center, top_left, bottom_left, top_right, bottom_right)
position = center

; Отображать секунды (true или false)
show_seconds = true

; Коэффициент увеличения ширины окна
width_increase_percent = 1.2

; Коэффициент увеличения высоты окна
height_increase_percent = 1.05

; Цвет полоски секунд
seconds_bar_color = #4C72AF

; Высота полоски секунд
seconds_bar_height = 3
"""
    with open(settings_path, 'w', encoding='utf-8') as file:
        file.write(settings_content)

# Функция для получения пути к файлу настроек
def get_settings_path() -> str:
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, SETTINGS_FILE)

# Функция для обновления времени
def update_time() -> None:
    if show_seconds:
        current_time = datetime.now().strftime('%H:%M:%S')
    else:
        current_time = datetime.now().strftime('%H:%M')
    time_label.config(text=current_time)
    update_seconds_bar()
    root.after(1000, update_time)

# Функция для обновления полоски секунд
def update_seconds_bar() -> None:
    current_second = datetime.now().second
    bar_width = (current_second / 60) * root.winfo_width()
    seconds_bar.place(x=0, y=root.winfo_height() - seconds_bar_height, width=bar_width, height=seconds_bar_height)

# Функция для установки размера и положения окна
def set_window_size_and_position(font_size: int, position: str) -> None:
    root.overrideredirect(True)
    update_window_size(font_size)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    if position == 'center':
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
    elif position == 'top_left':
        x = 0
        y = 0
    elif position == 'bottom_left':
        x = 0
        y = screen_height - window_height
    elif position == 'top_right':
        x = screen_width - window_width
        y = 0
    elif position == 'bottom_right':
        x = screen_width - window_width
        y = screen_height - window_height
    else:
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

    root.geometry(f"+{x}+{y}")

# Функция для обновления размера окна
def update_window_size(font_size: int) -> None:
    font = (font_name, font_size, font_style)
    time_label.config(font=font, text="00:00:00" if show_seconds else "00:00")
    time_label.update_idletasks()
    width = time_label.winfo_reqwidth() * float(width_increase_percent)
    height = time_label.winfo_reqheight() * float(height_increase_percent)
    root.geometry(f"{int(width)}x{int(height)}")

# Функция для завершения программы по двойному клику
def on_double_click(event) -> None:
    root.destroy()

# Функция для инициализации настроек
def initialize_settings() -> None:
    global bg_color, font_size, font_name, font_style, font_color, show_seconds, width_increase_percent, height_increase_percent, seconds_bar_color, seconds_bar_height, position
    bg_color = settings.get('Settings', BG_COLOR)
    font_size = settings.getint('Settings', FONT_SIZE)
    font_name = settings.get('Settings', FONT_NAME)
    font_style = settings.get('Settings', FONT_STYLE)
    font_color = settings.get('Settings', FONT_COLOR)
    show_seconds = settings.getboolean('Settings', SHOW_SECONDS)
    width_increase_percent = settings.getfloat('Settings', WIDTH_INCREASE_PERCENT)
    height_increase_percent = settings.getfloat('Settings', HEIGHT_INCREASE_PERCENT)
    seconds_bar_color = settings.get('Settings', SECONDS_BAR_COLOR)
    seconds_bar_height = settings.getint('Settings', SECONDS_BAR_HEIGHT)
    position = settings.get('Settings', POSITION)

# Загрузка настроек
settings_path = get_settings_path()
settings = load_settings()

# Создание главного окна
root = tk.Tk()
root.title("TopClock")
root.attributes("-topmost", True)

# Инициализация настроек
initialize_settings()

# Установка цвета фона из настроек
root.configure(bg=bg_color)

# Создание метки для отображения времени
time_label = tk.Label(root, font=(font_name, font_size, font_style), bg=bg_color, fg=font_color)
time_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Создание полоски секунд
seconds_bar = tk.Frame(root, bg=seconds_bar_color, height=seconds_bar_height)
seconds_bar.place(x=0, y=root.winfo_height() - seconds_bar_height, width=0, height=seconds_bar_height)

# Установка размера и положения окна
set_window_size_and_position(font_size, position)

# Обновление времени каждую секунду
update_time()

# Привязка двойного клика к функции завершения программы
root.bind("<Double-Button-1>", on_double_click)

# Запуск главного цикла
root.mainloop()
