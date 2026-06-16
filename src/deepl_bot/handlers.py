from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import (
    Message,
    ChatMemberUpdated,
    ChatMemberAdministrator,
    ChatMemberOwner,
)

from . import deepl
from .bot import bot
from db import repo

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Hi, {message.from_user.first_name}! To set a preferred language use /lang command. The default one is English"
    )


@router.my_chat_member()
async def on_bot_added(event: ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator"):
        await event.answer(
            "Hi! I'll help translate messages in this group. To set a preferred language use /lang command. The default one is English"
        )


@router.message(Command(commands=["lang"]))
async def set_lang(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(
            f"Please specify a language code\nTo list all available languages use /list command"
        )
    lang = command.args.split(" ")[0].upper()
    if lang not in deepl.langs:
        await message.answer(
            f"{lang} is not a valid language code\nTo list all available languages use /list command"
        )
    user_status = await bot.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    if (
        isinstance(user_status, ChatMemberAdministrator)
        or isinstance(user_status, ChatMemberOwner)
        or message.chat.type == "private"
    ):
        await repo.set_lang(message.chat.id, lang)
        await message.answer(f"Preferred language successfully set to {deepl.langs[lang]}")


@router.message(Command(commands=["list"]))
async def list_langs(message: Message):
    answer = f"Available languages:\n{'\n'.join(f'{code} - {name}' for code, name in deepl.langs.items())}"
    await message.answer(answer)


@router.message()
async def translate_message(message: Message):
    target_lang = await repo.get_lang(message.chat.id)

    res = await deepl.translate_text(message.text, target_lang)
    if res is None:
        return

    await message.reply(res)
