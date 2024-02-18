# Запуск

1. Скопировать файл .env.example в .env
2. Установить зависимости: `poetry install`
3. Заполнить недостающие значения в соотвествии с требованиями `pyrogram Client`
4. Запустить базу данных в docker compose: `docker compose up -d`
5. Запустить бота `python main.py`