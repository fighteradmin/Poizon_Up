import os

from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)  # Italic, as_numbered_list и тд
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard
from kbds.inline import get_url_btns, get_inlineMix_btns, start_kb, support

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

bot = Bot(token=os.getenv('TOKEN'))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker="CAACAgIAAxkBAAEEIwABZfh-ObKLuCOIyzpVK4MdHVw-c90AAqYAA1KJkSNruSoQjbfHvDQE",  reply_markup=get_keyboard(
            "Ассортимент",
            "О магазине",
            placeholder="Что вас интересует?",
            sizes=(1, 1)
        ),)
    await message.answer(f"<em>Здравствуйте, <b>{message.from_user.full_name}</b>! Я бот магазина FF Poizon. Я могу прислать подробные фото "
        f"о каждом товаре. Для этого выберите кнопкой ниже нужную категорию "
        f"и там найдите интересующий товар. Я скину всю информацию, которая у меня есть</em>", parse_mode="HTML")
    await message.answer_photo(photo="AgACAgIAAxkBAAP1ZfiCEEtdlVDwyHLDARPe8Mm4OqsAAqzXMRtn68lL27q7dPyIc58BAAMCAAN5AAM0BA",
                               caption="<em>Выберите нужную категорию</em>"
        , parse_mode="HTML",
                               reply_markup=start_kb)


# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}", parse_mode="HTML"
        )
    await message.answer("Вот меню:")


@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")

@user_private_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('Вы выбрали каталог')
    for product in await orm_get_products(session):
        await callback.message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}", parse_mode="HTML")
    return menu_cmd

@user_private_router.callback_query(F.data == 'help')
async def catalog(callback: CallbackQuery):
    await callback.answer('Помощь/Сотрудничество🫱🏻‍🫲🏻')
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBD2X4j-bZLgcuya9mnFegClruQuHkAAIM2DEbZ-vJSwj6qPjTUtE6AQADAgADeQADNAQ",
                                        caption="<b>По вопросам/Сотрудничеству</b>⬇️",
                                        parse_mode="HTML",
                                        reply_markup=support)

    return menu_cmd

# @user_private_router.message(F.photo)
# async def photo(message: types.Message):
#     photo_data = message.photo[-1]
#
#     await message.answer(f'{photo_data}')


# @user_private_router.message(F.contact)
# async def get_contact(message: types.Message):
#     await message.answer(f"номер получен")
#     await message.answer(str(message.contact))


# @user_private_router.message(F.location)
# async def get_location(message: types.Message):
#     await message.answer(f"локация получена")
#     await message.answer(str(message.location))
