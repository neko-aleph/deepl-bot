from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from .model import ChatLanguages
from .db import session_maker

async def set_lang(chat_id: int, lang: str):
    stmt = insert(ChatLanguages).values(chat_id=chat_id, lang=lang)
    stmt = stmt.on_conflict_do_update(
        index_elements=[ChatLanguages.chat_id],
        set_=dict(lang=stmt.excluded.lang)
    )

    async with session_maker() as session:
        await session.execute(stmt)
        await session.commit()


async def get_lang(chat_id: int) -> str:
    query = select(ChatLanguages).where(ChatLanguages.chat_id == chat_id)

    async with session_maker() as session:
        result = await session.execute(query)
        row = result.scalar_one_or_none()
        return row.lang if row else "EN"
