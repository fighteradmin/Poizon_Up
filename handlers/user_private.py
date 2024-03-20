import os
import random
import time

from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import CallbackQuery, message_id
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)  # Italic, as_numbered_list и тд
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_products, orm_get_categories
from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard
from kbds.inline import get_url_btns, get_inlineMix_btns, start_kb, support, get_callback_btns, user_product, prof_back, \
    generate_password, continue_reg, prof_back_not_reg

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

bot = Bot(token=os.getenv('TOKEN'))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker="CAACAgIAAxkBAAEEIwABZfh-ObKLuCOIyzpVK4MdHVw-c90AAqYAA1KJkSNruSoQjbfHvDQE",  reply_markup=get_keyboard(
            "О магазине",
            placeholder="Нажмите кнопку",
            sizes=(1, 1)
        ),)
    await message.answer(f"<em>Здравствуйте, <b>{message.from_user.full_name}</b>! Я бот магазина FF Poizon. Я могу прислать подробные фото "
        f"о каждом товаре. Для этого выберите кнопкой ниже нужную категорию "
        f"и там найдите интересующий товар. Я скину всю информацию, которая у меня есть</em>", parse_mode="HTML")
    await message.answer_photo(photo="AgACAgIAAxkBAAMKZfnUCkMyCun-u7I8I5C1sSH3th8AAqzXMRtn68lLhKA_z-tJVm8BAAMCAAN5AAM0BA",
                               caption="<em>Выберите нужную категорию</em>"
        , parse_mode="HTML", reply_markup=start_kb)


@user_private_router.callback_query(F.data.startswith('category_s'))
async def products_menu(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer('')
    category_id = callback.data.split('_s')[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)} ₽", parse_mode="HTML", reply_markup=user_product)
# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name: f'category_s{category.id}' for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns), parse_mode="HTML")


@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('Вы выбрали каталог')
    categories = await orm_get_categories(session)
    btns = {category.name: f'category_s{category.id}' for category in categories}
    await callback.message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns), parse_mode="HTML")

class Reg(StatesGroup):
    name = State()

@user_private_router.callback_query(F.data == 'register')
async def reg_one(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Reg.name)
    await callback.message.answer("<b>Введите ваше имя:</b>", parse_mode="HTML")

@user_private_router.message(Reg.name)
async def reg_two(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("<b>Сгенирируйте ключ</b>", reply_markup=generate_password, parse_mode="HTML")
    await state.clear()

@user_private_router.callback_query(F.data == 'gener_pass')
async def profile(callback: CallbackQuery):
    await callback.answer('')
    a = "abcdefghijklmnopqrstuvwxyz"
    b = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    c = "0123456789"
    d = "[]{}()*'/,_-!?"

    all = a + b + c + d
    length = 10

    password = "".join(random.sample(all, length))
    await callback.message.answer("<b>Идёт генерация ключа...</b>", parse_mode="HTML")
    time.sleep(3)
    await callback.message.delete()
    await callback.message.answer(f"<b>Ваш ключ:</b> " + password, reply_markup=continue_reg, parse_mode="HTML")

@user_private_router.callback_query(F.data == 'skip')
async def profile(callback: CallbackQuery):
    await callback.answer('Ваши данные защищены✅', show_alert=True)
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAANRZfno9HpWZXXFR7mD3xnbckIAAVeFAAKP2zEb91HQS0TEs73yiKJrAQADAgADeQADNAQ",
        caption=f"<b>Ваш ID:</b> <code>{callback.message.from_user.id}</code>\n\n"
                f"<b>Кол-во заказов:</b> <code>0</code>\n\n"
                f"<b>Скидка:</b> <code>0%</code>\n\n", parse_mode="HTML", reply_markup=prof_back_not_reg)


@user_private_router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    await callback.answer('')


    await callback.message.answer_photo(photo="AgACAgIAAxkBAANRZfno9HpWZXXFR7mD3xnbckIAAVeFAAKP2zEb91HQS0TEs73yiKJrAQADAgADeQADNAQ",
                                              caption=f"<b>Ваш ID:</b> <code>{callback.message.from_user.id}</code>\n\n"
                                                      f"<b>Кол-во заказов:</b> <code>0</code>\n\n"
                                                      f"<b>Скидка:</b> <code>0%</code>\n\n", parse_mode="HTML", reply_markup=prof_back)






@user_private_router.callback_query(F.data == 'help')
async def help(callback: CallbackQuery):
    await callback.answer('Помощь/Сотрудничество🫱🏻‍🫲🏻')
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMLZfnUCuT5-qgUUc02rPpQJUdwQRcAAgzYMRtn68lLoMfhECcV4Z8BAAMCAAN5AAM0BA",
                                        caption="<b>По вопросам/Сотрудничеству</b>⬇️",
                                        parse_mode="HTML",
                                        reply_markup=support)

    return menu_cmd


@user_private_router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAMKZfnUCkMyCun-u7I8I5C1sSH3th8AAqzXMRtn68lLhKA_z-tJVm8BAAMCAAN5AAM0BA",
        caption="<em>Выберите нужную категорию</em>"
        , parse_mode="HTML",
        reply_markup=start_kb)


@user_private_router.message(F.text == 'Меню')
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name : f'category_s{category.id}' for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns), parse_mode="HTML")



# @user_private_router.message(F.photo)
# async def photo(message: types.Message):
#     photo_data = message.photo[-1]
#
#     await message.answer(f'{photo_data}')


