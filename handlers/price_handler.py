from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# from magic_filter import F

router = Router()


class FSMPrice(StatesGroup):
    age = State()
    engine = State()
    power = State()
    capacity = State()
    price = State()


@router.callback_query(F.data == 'price')
async def get_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        '🚗 Возраст автомобиля?',
    )
    await state.set_state(FSMPrice.age)
