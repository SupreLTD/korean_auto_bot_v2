from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards.start_kb import main


router = Router()


@router.message(Command(commands=['start']))
async def start_bot(message: types.Message):
    await message.answer(f'🖐 Привет, {message.from_user.username}!\n\n '
                         f'Меня Зовут Avto_bot!🤖 \n\nЯ Telegram-бот для расчета привоза корейских автомобилей, я помогу '
                         f'рассчитать цену и другие детали по доставке автомобиля.\n\n'
                         f'💰 Я предоставляю такую информацию, как цены, характеристики и спецификации для различных '
                         f'моделей автомобилей корейских производителей.', reply_markup=main())