import aiohttp
import pytest

from legibot2.alison import AlisonApi


async def test_bill_count(api):
    result = await api.get_bill_count()
    assert result > 0


async def test_bill_summaries(api):
    result = await api.get_all_bill_summaries(limit=35)
    assert len(result) > 25
    numbers = [x["InstrumentNbr"] for x in result]
    assert len(set(numbers)) == len(numbers)
    assert "HB11" in set(numbers)


@pytest.fixture
async def api():
    async with aiohttp.ClientSession() as session:
        yield AlisonApi(session)
