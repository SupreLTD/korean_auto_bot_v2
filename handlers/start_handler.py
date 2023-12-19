from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards.start_kb import main

router = Router()


@router.callback_query(F.data == 'start')
@router.message(Command(commands=['start']))
async def start_bot(message: types.Message | types.CallbackQuery):
    answer = f'Меня Зовут Avto_bot!🤖 \n\nЯ Telegram-бот для расчета привоза корейских автомобилей, я помогу ' \
             f'рассчитать цену и другие детали по доставке автомобиля.\n\n' \
             f'💰 Я предоставляю такую информацию, как цены, характеристики и спецификации для различных ' \
             f'моделей автомобилей корейских производителей.'

    if message.__class__ is types.Message:
        await message.answer(f'🖐 Привет, {message.from_user.username}!\n\n {answer}', reply_markup=main())
    elif message.__class__ is types.CallbackQuery:
        await message.message.answer(f'🖐 Привет, {message.from_user.username}!\n\n {answer}', reply_markup=main())
