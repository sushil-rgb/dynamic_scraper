from fake_useragent import UserAgent
import pandas as pd
import itertools
import aiohttp
import secrets
import yaml
import os


class Response:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'User-Agent': user_agents()}
    
    async def response(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers = self.headers) as resp:
                cont = resp.status
                return cont
    
    async def content(self):
        async with aiohttp.ClientSesssion() as session:           
            async with session.get(self.base_url, headers = self.headers) as resp:
                cont = await resp.read()
                return cont


class TryExcept:
    async def text(self, element):
        try:
            elements = (await (await element).inner_text()).strip()
        except AttributeError:
            elements = "N/A"
        return elements
        
    async def attributes(self, element, attr):
        try:
            elements = await (await element).get_attribut(attr)
        except AttributeError:
            elements = "N/A"
        return elements


async def filter_data(raw_lists):
    filtered_lists = []
    for data in raw_lists:
        if not data in filtered_lists:
            filtered_lists.append(data)
    return filtered_lists


async def list_flattened(multdimensional_lists):
    return list(itertools.chain(*multdimensional_lists))


async def create_path(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)
    if os.path.exists(directory_path):
        pass
    else:
        os.mkdir(directory_path)


async def export_sheet(dictionary_name, sheet_name):
    directory_name = "Scraped datasets"
    await create_path(directory_name)
    df = pd.DataFrame(dictionary_name)
    df.to_excel(f"""{os.getcwd()}//{directory_name}//{sheet_name}.xlsx""", index = False)
    print(f"{sheet_name} saved.")


async def random_values(datas_lists):
    indexes = secrets.randbelow(len(datas_lists))
    return datas_lists[indexes]


async def random_time(value):
    ranges = [i for i in range(0, value + 1)]
    return random_values(ranges)


async def user_agents():
    agents = UserAgent()
    return agents.random


async def load_selectors(selectors):
    with open(f"{selectors}.yaml") as file:
        selects = yaml.load(file, Loader = yaml.SafeLoader)
        return selects

