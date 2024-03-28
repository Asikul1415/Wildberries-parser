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


    async def parse(self,page: int,session: aiohttp.ClientSession) -> None:
        url = self.url.replace(f'&page=1',f'&page={page}')
        
        async with session.get(url=url) as response:
            html = await response.text()
            status_code = response.status
            
            if(status_code != 200):  
                print(f"[x] страница №{page} HTTP {status_code}")
                await self.parse(page=page,session=session)
            elif html == '':
                return
            else:
                json = await response.json()
                product_temp = models.Items.parse_obj(obj = json['data'])
                self.products.append(product_temp)

                print(f"[v] страница №{page}")
        
    

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
        df = pd.DataFrame(self.__get_products(Items=Items))
        writer = pd.ExcelWriter('wb_data.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Продукты',index=False,na_rep='NaN')

        #автоматическая подстройка размеров колонок в excel
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Продукты'].set_column(col_idx, col_idx, column_length)
        
        writer.close()
    
    async def gather_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = []

            for page in range(1,self.pages_count + 1):
                task = asyncio.create_task(self.parse(page=page,session=session))
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
    
    
                

url = 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/dzhinsy'
start = time.time()

test = Parser(url=url,pages_count=120)
asyncio.run(test.gather_data())
test.save_to_excel(Items= test.products)

end = time.time()
print(f"Парсинг занял {round(end - start,4)} с")
    
