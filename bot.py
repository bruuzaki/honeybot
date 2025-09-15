import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from storage import init_db, add_user, remove_user, list_users, get_all_chat_ids
from scheduler import schedule_jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ------------------ Configuración ------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
REGISTER_CODE = os.getenv("REGISTER_CODE", "mi-codigo-secreto")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) if os.getenv("ADMIN_ID") else None
TZ = os.getenv("TZ", "America/Montevideo")
SEND_HOUR = int(os.getenv("SEND_HOUR", "20"))

if not BOT_TOKEN:
    raise RuntimeError("Necesitas definir BOT_TOKEN en las variables de entorno")

# ------------------ Logging ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------ Helper ------------------
async def send_message(application, chat_id: int, text: str):
    try:
        await application.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
    except Exception as e:
        logger.exception(f"Error enviando mensaje a {chat_id}")

# ------------------ Handlers ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy HoneyBot. Para registrarte usa /register <codigo>\n"
        "Ejemplo: /register mi-codigo-secreto"
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) == 0:
        await update.message.reply_text("Debes enviar el código secreto. /register <codigo> [nombre]")
        return

    code = args[0]
    name = " ".join(args[1:]) if len(args) > 1 else update.effective_user.full_name

    if code != REGISTER_CODE:
        await update.message.reply_text("Código incorrecto.")
        return

    await add_user(update.effective_chat.id, name)
    await update.message.reply_text("Registrado correctamente. Recibirás recordatorios el 11 y el 22 de cada mes. ❤️")

async def unregister(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await remove_user(update.effective_chat.id)
    await update.message.reply_text("Te he eliminado de la lista de recordatorios.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and update.effective_chat.id != ADMIN_ID:
        await update.message.reply_text("Comando reservado al admin.")
        return

    users = await list_users()
    if not users:
        text = "No hay usuarios registrados."
    else:
        text = "Usuarios registrados:\n" + "\n".join([f"- {r[1]} ({r[0]})" for r in users])
    await update.message.reply_text(text)

async def send_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and update.effective_chat.id != ADMIN_ID:
        await update.message.reply_text("Comando reservado al admin.")
        return

    chat_ids = await get_all_chat_ids()
    message = "Mensaje de prueba manual. Si lo recibes, el bot está funcionando."
    for cid in chat_ids:
        await context.application.bot.send_message(chat_id=cid, text=message)
    await update.message.reply_text("Envíos de prueba realizados.")

# ------------------ Main ------------------
async def init_bot():
    await init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("unregister", unregister))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("send_test", send_test))

    # Scheduler
    scheduler = AsyncIOScheduler(timezone=TZ)
    schedule_jobs(scheduler, lambda cid, msg: send_message(app, cid, msg), tz_name=TZ, hour=SEND_HOUR)

    return app

# ------------------ Entry point ------------------
if __name__ == "__main__":
    import asyncio
    app = asyncio.run(init_bot())
