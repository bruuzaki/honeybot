from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import asyncio
from storage import get_all_chat_ids

# ------------------ Scheduler ------------------
def schedule_jobs(scheduler: AsyncIOScheduler, send_callback, tz_name="America/Montevideo", hour=20):
    """
    schedule_jobs: programa los recordatorios los días 11 y 22 a la hora indicada.
    send_callback: función async(chat_id, message)
    """
    tz = pytz.timezone(tz_name)

    trigger = CronTrigger(day='11,22', hour=hour, minute=0, timezone=tz)

    # Job wrapper async
    async def job_wrapper():
        chat_ids = await get_all_chat_ids()
        message = build_message()
        for cid in chat_ids:
            try:
                await send_callback(cid, message)
            except Exception as e:
                print(f"[Scheduler] Error enviando mensaje a {cid}: {e}")

    # Agregamos job
    scheduler.add_job(lambda: asyncio.create_task(job_wrapper()), trigger=trigger, id="honey_reminder")
    scheduler.start()

# ------------------ Mensaje ------------------
def build_message():
    return (
        "📯 *Recordatorio de vela de miel*\n\n"
        "Hoy es día para prender la vela de miel. 🕯️🍯\n\n"
        "Un beso grande ❤️\n\n"
        "_Enviado por HoneyBot_"
    )
