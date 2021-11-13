import asyncio
import services.update_db as update
TIME_INTERVAL_IN_SEC = 60


async def async_update():
    while True:
        update.update_all()
        await asyncio.sleep(TIME_INTERVAL_IN_SEC)


def sinc_server():
    loop = asyncio.get_event_loop()
    task = loop.create_task(async_update())
    loop.run_until_complete(task)
