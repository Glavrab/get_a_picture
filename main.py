from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio


URL = 'https://www.generatormix.com/random-image-generator'


def html_parser(data: str, object_to_find: str, **search_args) -> str:
    """Parse html page to look for object"""
    parsed_html_doc = BeautifulSoup(data, 'lxml')
    searched_str = parsed_html_doc.find_all(attrs=search_args)
    for attr in searched_str:
        info = attr.get(object_to_find)
        return info


async def get_picture(num: int) -> None:
    """Get a random picture from the website"""
    session = ClientSession()
    async with session.get(URL) as response:
        html_doc = await response.text()
        token = html_parser(data=html_doc, object_to_find='value', type='hidden')
        data = {'_token': token}
        for i in range(num):
            response = await session.post(URL, data=data)
            unparsed_response = await response.text()
            unparsed_url_for_picture = html_parser(data=unparsed_response[27:-2], object_to_find='data-src', src=True)
            image_name = unparsed_url_for_picture[30:-2]
            url_for_picture = 'https://pixabay.com/get/' + image_name
            async with session.get(url_for_picture) as response_picture:
                picture = await response_picture.content.read()
                filename = image_name
                with open(filename, 'xb') as new_picture:
                    new_picture.write(picture)
    await session.close()


if __name__ == '__main__':
    pictures_to_download = int(input('How many pictures do you want?'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_picture(pictures_to_download))
    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
