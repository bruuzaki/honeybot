# HoneyBot — Telegram reminders

Bot de Telegram que manda recordatorios los días 11 y 22 de cada mes para “prender la vela de miel”.

## Características
- Registro seguro mediante `REGISTER_CODE`.
- Base de datos SQLite (aiosqlite).
- Scheduler con APScheduler (cron 11 y 22).
- Docker + docker-compose para despliegue 24/7.
- Ready para correr en Proxmox LXC / VM.

## Tecnologías
- Python 3.11
- python-telegram-bot 22.4
- APScheduler 3.11.0
- aiosqlite 0.21.0
- python-dotenv 1.1.1
- Docker

## Cómo usar (desarrollo)
1. Copiar `.env.example` a `.env` y completar variables (NO subir `.env` a Git).
2. Entorno local:
```bash
pip install -r requirements.txt
python bot.py
