from asyncio import gather, wait_for, sleep
from json import loads
import aiofiles

from app.config import settings


async def collect_data():
    tasks = [
        exception_filter(get_data_from_source('data1.json')),
        exception_filter(get_data_from_source('data2.json', 0)),
        exception_filter(get_data_from_source('data3.json', 1))
    ]
    res = await gather(*tasks)
    temp = []
    for list_data in res:
        for item in list_data:
            temp.append(item)
    return sorted(temp, key=lambda x: x['id'])


async def get_data_from_source(name_file, mode=None):
    if mode == 0:  # Режим 0 - Имитация исключения во время получения данных
        raise Exception("Test")
    if mode == 1:  # Режим 1 - Имитация задержи ответа более дозволенного
        await sleep(3)

    async with aiofiles.open(settings.PATH_TO_SOURCE + name_file) as f:
        data = loads(await f.read())
        await f.close()
    return data


async def exception_filter(function):
    try:
        return await wait_for(function, timeout=2)
    except Exception:
        return []
