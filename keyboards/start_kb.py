from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def main():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text='Через ссылку на encar', callback_data='link'),
        types.InlineKeyboardButton(text='Через ввод цены', callback_data='price'),
    )

    return kb.as_markup()