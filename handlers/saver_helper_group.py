import re
from typing import Any
from contextlib import suppress
from datetime import datetime, timedelta

from aiogram import Bot, types, Router, F
from aiogram.types import ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from filters.chat_types import ChatTypeFilter




saver_helper_router = Router()
saver_helper_router.message.filter(F.chat_type == "supergroup", F.from_user.id == 6769098861)


def parse_time(time_string: str | None) -> datetime | None:
    global time_delta
    if not time_string:
        return None

    match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
    current_datetime = datetime.utcnow()

    if match_:
        value = int(match_.group(1))
        unit = match_.group(2)

        match unit:
            case "h": time_delta = timedelta(hours=value)
            case "d": time_delta = timedelta(days=value)
            case "w": time_delta = timedelta(weeks=value)
            case "_": return None
    else:
        return None

    new_datetime = current_datetime + time_delta
    return new_datetime

@saver_helper_router.message(Command("ban"))
async def ban(message: types.Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        return await message.answer("<em>Пользователь не найден!</em>", parse_mode="HTML")

    until_date = parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(
            chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date
        )
        await message.answer(f"<em>Пользователя</em> <b>{mention}</b> <em>заблокировали!</em>", parse_mode="HTML")






@saver_helper_router.message(Command("mute"))
async def mute(message: types.Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        return await message.answer("<em>Пользователь не найден!</em>", parse_mode="HTML")

    until_date = parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(f"<em>Пользователя</em> <b>{mention}</b> <em>замутили!</em>", parse_mode="HTML")





























