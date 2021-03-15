from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio


URL = 'https://www.generatormix.com/random-image-generator'


async def get_picture(num: int) -> None:
    """Get a random picture from the website"""
    session = ClientSession()
    async with session.get(URL) as response:
        html_doc = await response.text()
        parsed_html_doc = BeautifulSoup(html_doc, 'html.parser')
        str_with_token = parsed_html_doc.find(value=True, type='hidden')
        token = str(str_with_token)[42:82]
        data = {'_token': token}
        for i in range(num):
            response = await session.post(URL, data=data)
            unparsed_response = await response.json()
            html_doc = BeautifulSoup(unparsed_response['output'], 'html.parser')
            list_of_attr = html_doc.find_all(src=True)
            for attr in list_of_attr:
                url_for_picture = attr.get('data-src')
                async with session.get(url_for_picture) as response_picture:
                    picture = response_picture.content.read()
                    filename = url_for_picture[24:-2] + 'jpg'
                    with open(filename, 'w'):
                        filename.write(picture)
    await session.close()


