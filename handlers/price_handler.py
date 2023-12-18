import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal

from keyboards import price_kb as KB
from parsers.exchange_rates import get_rates
from parsers.tax import get_tax

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
    await state.update_data(age_answer=callback_data.answer)
    await call.message.edit_text(f'🚗 Возраст автомобиля?\n\n✅ Ответ: {callback_data.answer}')
    await call.message.answer('🚕 Тип двигателя?', reply_markup=KB.engine_choose())
    await state.set_state(FSMPrice.engine)


@router.callback_query(KB.PriceChoose.filter(F.action == 'engine'))
async def get_power(call: types.CallbackQuery, callback_data: KB.PriceChoose, state: FSMContext):
    await state.update_data(engine=callback_data.data)
    await state.update_data(engine_answer=callback_data.answer)
    await call.message.edit_text(f'🚕 Тип двигателя?\n\n✅ Ответ: {callback_data.answer}')
    await call.message.answer('🏎 Мощность двигателя (л.с.)?')
    await state.set_state(FSMPrice.power)


@router.message(FSMPrice.power)
async def get_capacity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(power=message.text)
        await state.update_data(power_answer=message.text)
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
        rates = await get_rates()
        price = Decimal(message.text) * rates.KRW
        tax = await get_tax(age, engine, power, capacity, message.text)
        spending_in_korea = (1500 * rates.USD) * Decimal('1.03')  # НАСТРАИВАЕТСЯ
        kom_ru = 50000
        delivery = 300000
        car_price_rub = price * Decimal('1.055')
        total = spending_in_korea + kom_ru + tax.tax + delivery + car_price_rub

        result_message = f'🕵️ Ваш запрос: 👇\n🚗 Возраст автомобиля: {fsm_data["age_answer"]}\n' \
                          f'🚕 Тип двигателя: {fsm_data["engine_answer"]}\n🏎 Мощность двигателя: {power} л.с.\n' \
                          f'🚙 Объем двигателя: {capacity} м3\n💰 Стоимость автомобиля в руб: {float(car_price_rub):.02f}\n\n' \
                          f'Расчет с учетом курса валют:\n1 ₽ = {rates.KRW:.02f} ₩\n1 ₩ = {1/rates.KRW} ₽\n' \
                          f'1 $ = {rates.USD:.02f} ₽\n' \
                          f'* Курс валют актуален на: {datetime.datetime.now().replace(microsecond=0)}\n' \
                          f'с сайта ЦБ РФ\n\n' \
                          f'• Таможенный сбор: {tax.sbor} ₽\n• Утилизационный сбор: {tax.util} ₽\n' \
                          f'• Таможенная пошлина: {tax.tax} ₽\n• Расходы в Корее: {spending_in_korea:.02f}\n' \
                          f'• Комиссия РФ: {kom_ru} ₽\n' \
                          f'• Доставка {delivery} ₽\n\n ✅ Итоговая стоимость автомобиля: {total}'




    else:
        await message.answer('Введите корректное значение!')
    await message.delete()
