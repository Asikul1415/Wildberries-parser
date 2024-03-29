import os
import requests
import time
import models
import pandas as pd
import asyncio
import aiohttp

class Parser: 

    def __init__(self,url:str,pages_count: int):
        self.url = self.__get_url(url= url)
        self.pages_count = pages_count 
        self.products = []
        self.pages = asyncio.Queue()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/aksessuary/zonty',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',}
    
    def __get_url(self,url: str) -> str:
        parameters = []
        if('?' in url):
            parameters_temp = url.split('?')[1]
            parameters = parameters_temp.split('&')
            
        url = url.split('?')[0]

        wb_basket = self.__get_wb_basket()
        catalogs = self.__get_catalogs(wb_basket=wb_basket)
        
        request_url = f"{self.__get_request_link(catalogs,url=url)}&page=1&appType=1&curr=rub&dest=-1611682&spp=30&limit=300"
        for parameter in parameters:
            if('page=' not in parameter):
                request_url += f"&{parameter.removeprefix('f')}"
            else:
                request_url.replace('page=1',parameter)
        return request_url

    def __get_wb_basket(self) -> list:
        return requests.get(url = 
        'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json').json()

    def __get_catalogs_data(self,catalog: list) -> list:
        catalog_data = []

        if('childs' in catalog):
            for child in catalog['childs']:
                catalog_data.extend(self.__get_catalogs_data(child))
            return catalog_data

        elif('shard' in catalog and 'query' in catalog and 'url' in catalog):
            return [{
                'shard': catalog['shard'],
                'query': catalog['query'],
                'url' : catalog['url']}]
        else:
            return ['blackhole']
    
    def __get_catalogs(self,wb_basket: dict):
        catalogs = []

        for catalog in wb_basket:
            child_data = self.__get_catalogs_data(catalog= catalog)
            catalogs.extend(child_data)

        return catalogs

    def __get_request_link(self, catalogs: list,url: str) -> str:
        for catalog in catalogs:
            if('shard' in catalog and 'query' in catalog):
                if(catalog['url'] == url.split('https://www.wildberries.ru')[1]):
                    return f"https://catalog.wb.ru/catalog/{catalog['shard']}/v2/catalog?{catalog['query']}"


    async def parse_page(self,page: int,session: aiohttp.ClientSession, attempts = 5) -> None:
        url = self.url.replace(f'&page=1',f'&page={page}')
        await asyncio.sleep(2)
        
        async with session.get(url=url) as response:
            html = await response.text()
            status_code = response.status
            
            if(status_code != 200) or (status_code == 200 and html == ''):  
                print(f"[x] страница №{page} HTTP {status_code}")
                if (status_code == 200 and html == ''):
                    await self.parse_page(page=page,session=session,attempts=attempts-1)
                else:
                    await self.parse_page(page=page,session=session)
            elif html == '' and attempts > 0:
                return
            else:
                json = await response.json()
                product_temp = models.Items.parse_obj(obj = json['data'])
                self.products.append(product_temp)
                print(f"[v] страница №{page}")

    async def parse(self,page:int, session: aiohttp.ClientSession) -> None:
        async with asyncio.Semaphore(2):
            page = await self.pages.get()
            await self.parse_page(page=page,session=session)
            await asyncio.sleep(2)

    

    def __get_products(self,Items : list[models.Items]) -> list[dict]:
        products = []

        for page in Items:
            for product in page.products:
                products.append({
                    'id' : product.id,
                    'Ссылка' :  f'https://www.wildberries.ru/catalog/{product.id}/detail.aspx',
                    'Бренд' : product.brand,
                    'id бренда' : product.brandId,
                    'Название продукта' : product.name,
                    'Рейтинг товара' : product.reviewRating,
                    'Кол-во отзывов о товаре' : product.feedbacks,
                    'В наличии' : product.volume,
                    'Цена без скидки' : product.sizes[0].price.basic,
                    'Цена со скдикой' : product.sizes[0].price.total,   
                    'Название поставщика' : product.supplier,
                    'id поставщика' : product.supplierId,
                    'Рейтинг поставщика' : product.supplierRating,
                }) 
        return products   

    def save_to_excel(self, Items: list[dict]) -> None:
        print("Формирование файла wb_data.xlsx ...")
        df = pd.DataFrame(self.__get_products(Items=Items))
        writer = pd.ExcelWriter(f'{self.path}\wb_data.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Продукты',index=False,na_rep='NaN')

        #автоматическая подстройка размеров колонок в excel
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Продукты'].set_column(col_idx, col_idx, column_length)
        print(f"\nВсё спарсилось, ищите wb_data.xlsx по пути {self.path}\wb_data.xlsx")
        writer.close()
    
    async def gather_data(self):
        async with aiohttp.ClientSession(headers=self.headers,
            connector=aiohttp.TCPConnector(limit=2)) as session:
            tasks = []
            
            if(self.pages_count > 100):
                self.pages_count = 100
            for page in range(1,self.pages_count + 1):
                await self.pages.put(page)
                task = asyncio.create_task(self.parse(page=page,session=session))
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
    
    
                

os.system('cls')
url = input("Вставьте ссылку на каталог: ")
pages_count = int(input("\nСколько страниц парсить? (больше 100 сервера не отдают): "))

start = time.time()

parser = Parser(url=url, pages_count=pages_count)
asyncio.run(parser.gather_data())
parser.save_to_excel(Items=parser.products)

end = time.time()
print(f"\nПарсинг занял {round(end - start,4)} с")
time.sleep(5)
    
