import os
import sys

# Добавляем текущую директорию в sys.path для правильного импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем Flask-приложение
from main import app

# Для Gunicorn
application = app

if __name__ == "__main__":
    app.run()
