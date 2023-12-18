from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import MagicData
from keyboards import price_kb as KB

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
        reply_markup=KB.age_choose()
    )
    await state.set_state(FSMPrice.age)


@router.callback_query(KB.PriceChoose.filter(F.action == 'age'))
async def get_engine(call: types.CallbackQuery, callback_data: KB.PriceChoose, state: FSMContext):
    await state.update_data(age=callback_data.data)
    await call.message.edit_text(f'🚗 Возраст автомобиля?\n\n✅ Ответ: {callback_data.answer}')
    await call.message.answer('🚕 Тип двигателя?', reply_markup=KB.engine_choose())
    await state.set_state(FSMPrice.engine)


@router.callback_query(KB.PriceChoose.filter(F.action == 'engine'))
async def get_power(call: types.CallbackQuery, callback_data: KB.PriceChoose, state: FSMContext):
    await state.update_data(engine=callback_data.data)
    await call.message.edit_text(f'🚕 Тип двигателя?\n\n✅ Ответ: {callback_data.answer}')
    await call.message.answer('🏎 Мощность двигателя (л.с.)?')
    await state.set_state(FSMPrice.power)


@router.message(FSMPrice.power)
async def get_capacity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(power=message.text)
        await message.answer(f'🏎 Мощность двигателя (л.с.)?\n\n✅ Ответ: {message.text} (л.с.)')
        await message.answer('🚙 Объем двигателя см3 (1 л = 1000 см3)?')
        await state.set_state(FSMPrice.capacity)
    else:
        await message.answer('Введите корректное значение!')
    await message.delete()


@router.message(FSMPrice.capacity)
async def get_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(capacity=message.text)
        await message.answer(f'🚙 Объем двигателя см3 (1 л = 1000 см3)??\n\n✅ Ответ: {message.text} (см3)')
        await message.answer('💰 Стоимость автомобиля в Вонах (₩)')
        await state.set_state(FSMPrice.price)
    else:
        await message.answer('Введите корректное значение!')
    await message.delete()


@router.message(FSMPrice.price)
async def result(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        fsm_data = await state.get_data()
        age = fsm_data['age']
        engine = fsm_data['engine']
        power = fsm_data['power']
        capacity = fsm_data['capacity']
        price = message.text
        # await message.answer(f'{age} {engine} {capacity} {power} {price}')

    else:
        await message.answer('Введите корректное значение!')
    await message.delete()
