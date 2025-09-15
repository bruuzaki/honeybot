from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import asyncio
from datetime import datetime
from storage import get_all_chat_ids

# job to send message; we will inject a send function when arrancamos el bot
def schedule_jobs(scheduler: AsyncIOScheduler, send_callback, tz_name="America/Montevideo", hour=20):
    tz = pytz.timezone(tz_name)

    # Cron trigger for day 11 and 22 at a given hour (local tz)
    trigger = CronTrigger(day='11,22', hour=hour, minute=0, timezone=tz)
    scheduler.add_job(func=lambda: asyncio.run(send_to_all(send_callback)), trigger=trigger, id="honey_reminder")
    scheduler.start()

async def send_to_all(send_callback):
    # get chat ids from DB
    chat_ids = await get_all_chat_ids()
    message = build_message()
    for cid in chat_ids:
        try:
            await send_callback(cid, message)
        except Exception as e:
            print(f"Error enviando a {cid}: {e}")

def build_message():
    return ("📯 *Recordatorio de vela de miel*\n\n"
            "Hoy es día para prender la vela de miel. 🕯️🍯\n\n"
            "Un beso grande ❤️\n\n"
            "_Enviado por HoneyBot_")
