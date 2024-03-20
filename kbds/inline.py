from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


# Создать микс из CallBack и URL кнопок
def get_inlineMix_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Товары🗓", callback_data="catalog")
        ],
{
            InlineKeyboardButton(text="Профиль💠", callback_data="profile")
        },
        {
            InlineKeyboardButton(text="Помощь🔒", callback_data="help")
        },
        {
            InlineKeyboardButton(text="Отзывы🔰", url="https://t.me/ff_poizon_otzivi")
        },
        {
            InlineKeyboardButton(text="Канал💕", url="https://t.me/ff_poizon")
        },
    ],
)

support = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вопросы❓", url="https://t.me/official_supp_t")
        ],
        {
            InlineKeyboardButton(text="Сотрудничество👋🏻", url="https://t.me/nastyalovekl")
        },
        {
            InlineKeyboardButton(text="Назад🔙", callback_data="back")
        }
    ],
)

user_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказать⚜️", url="https://t.me/official_supp_t")
        ],
        {
            InlineKeyboardButton(text="Главная панель⏏️", callback_data="back")
        },

    ],
)

prof_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Защита данных🔹", callback_data="register")
        ],
        {
            InlineKeyboardButton(text="Назад🔙", callback_data="back")
        }
    ]
)

prof_back_not_reg = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад🔙", callback_data="back")
        ],
    ]
)


generate_password = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сгенирировать ключ⚡️", callback_data="gener_pass")
        ],
    ],
)

continue_reg = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить💫", callback_data="skip")
        ],
    ],
)