from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


class PriceChoose(CallbackData, prefix='p'):
    action: str
    data: str
    answer: str


def age_choose():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text='до 3 лет', callback_data=PriceChoose(
            action='price',
            answer='до 3 лет',
            data='0-3').pack()),
        types.InlineKeyboardButton(text='от 3 до 5 лет', callback_data=PriceChoose(
            action='price',
            answer='от 3 до 5 лет',
            data='3-5').pack())
    )
    kb.row(
        types.InlineKeyboardButton(text='от 5 до 7 лет', callback_data=PriceChoose(
            action='price',
            answer='от 5 до 7 лет',
            data='5-7').pack()),
        types.InlineKeyboardButton(text='старше 7 лет', callback_data=PriceChoose(
            action='price',
            answer='старше 7 лет',
            data='7-0').pack())
    )

    return kb.as_markup()


def engine_choose():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text='Бензин', callback_data=PriceChoose(
            action='price',
            answer='Бензин',
            data='1').pack()),
        types.InlineKeyboardButton(text='Дизель', callback_data=PriceChoose(
            action='price',
            answer='Дизель',
            data='2').pack())
    )
    kb.row(
        types.InlineKeyboardButton(text='Гибрид', callback_data=PriceChoose(
            action='price',
            answer='Гибрид',
            data='3').pack()),
        types.InlineKeyboardButton(text='Электрический', callback_data=PriceChoose(
            action='price',
            answer='Электрический',
            data='4').pack())
    )

    return kb.as_markup()
