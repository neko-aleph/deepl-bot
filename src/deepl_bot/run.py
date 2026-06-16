import asyncio

from db import db
from .bot import bot, dp
from .handlers import router
from . import deepl


async def main():
    dp.include_router(router)

    try:
        await db.init_db()
        await deepl.get_languages()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
