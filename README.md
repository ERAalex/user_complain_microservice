# Complaint Classification API

Приложение на FastAPI для обработки пользовательских жалоб с использованием внешних сервисов для:
- анализа тональности,
- определения категории (AI),
- определения страны по IP.

- async

## 🔧 Технологии

- FastAPI
- SQLAlchemy
- PostgreSQL (или SQLite)
- Docker (n8n)
- n8n (автоматизация обработки жалоб)
- Telegram Bot API
- Внешние сервисы (IP API, Sentiment API, AI)

- Добавлено логгирование в ключевых моментах
---

## 📦 Установка и запуск
подготовьте .env (env.example)

Fast Api
uvicorn src.main:app --host 0.0.0.0 --port 8000

```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
