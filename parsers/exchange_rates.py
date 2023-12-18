from xml.etree import ElementTree
from decimal import Decimal
from dataclasses import dataclass
from aiohttp import ClientSession


@dataclass(slots=True)
class Currency:
    KRW: Decimal
    USD: Decimal


async def get_rates() -> Currency:
    async with ClientSession() as session:
        async with session.get('http://www.cbr.ru/scripts/XML_daily.asp') as response:
            r = await response.text()
            xml = ElementTree.fromstring(r)

            result = {
                'rates': [],
            }

            for currency in xml:
                props = {}
                for prop in currency:
                    props[prop.tag] = prop.text

                par = Decimal(props['Nominal'])
                par_value = Decimal(props['Value'].replace(',', '.'))

                result['rates'].append(
                    (
                        props['CharCode'],
                        par_value / par,)
                )
            result = {i[0]: i[1] for i in result['rates'] if i[0] in ('KRW', 'USD')}

            return Currency(**result)



