import json
from pydantic import BaseModel, field_validator
from decimal import Decimal

from aiohttp import ClientSession


class Tax(BaseModel):
    sbor:str
    tax: str
    util: str
    total: str

    @field_validator('sbor')
    def set_sbor(cls, value):
        return Decimal(value.replace(' ', ''). replace(',', '.'))

    @field_validator('tax')
    def set_tax(cls, value):
        return Decimal(value.replace(' ', '').replace(',', '.'))

    @field_validator('util')
    def set_util(cls, value):
        return Decimal(value.replace(' ', '').replace(',', '.'))

    @field_validator('total')
    def set_total(cls, value):
        return Decimal(value.replace(' ', '').replace(',', '.'))


async def get_tax(age: str, engine: str, power: str, capacity: str, price: str) -> Tax:
    data = {"owner": "1",
            "age": age,
            "engine": engine,
            "power": power,
            "power_unit": "1",
            "value": capacity,
            "price": price,
            "currency": "KRW"}

    async with ClientSession() as session:
        async with session.post(url='https://calcus.ru/rastamozhka-auto', data=data) as response:
            data = json.loads(await response.text(encoding='utf-8'))

            return Tax(**data)

