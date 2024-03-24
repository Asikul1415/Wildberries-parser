import requests
import time
import models
import pandas as pd

class Parser: 

    def __init__(self,cURL:str):
        self.url = self.__get_url(cURL= cURL)
    
    def __get_url(self,cURL: str) -> str:
        url = cURL.split('\'')[1]
        if '&page=' not in url:
            url += '&page=1'
        return url 

    def parse(self,pages_count: int) -> None:
        page = 1
        products = []

        while page <= pages_count:
            if(page != 1): 
                self.url = self.url.replace(f'&page={page-1}',f'&page={page}')
            response = requests.get(url = self.url)
            print(response.status_code)
            print(self.url)
            if(response.status_code == 429):
                print(response.content)
                time.sleep(5)
                page -= 1
            elif response.status_code == 500:
                response = requests.get(url = self.url)
            else:
                product = models.Items.parse_obj(obj = response.json()['data'])
                if not product:
                    break
                products.append(product)
            page += 1
            
        self.__save_to_excel(Items= products)
    

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
                    'Название поставщика' : product.supplier,
                    'id поставщика' : product.supplierId,
                    'Рейтинг поставщика' : product.supplierRating,
                    'Рейтинг товара' : product.reviewRating,
                    'Кол-во отзывов о товаре' : product.feedbacks,
                    'В наличии' : product.volume,
                    'Цена без скидки' : product.sizes[0].price.basic,
                    'Цена со скдикой' : product.sizes[0].price.total    
                }) 
        return products   

    def __save_to_excel(self, Items: list[dict]) -> None:
        df = pd.DataFrame(self.__get_products(Items=Items))
        writer = pd.ExcelWriter('wb_data.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Продукты',index=False,na_rep='NaN')

        #автоматическая подстройка размеров колонок в excel
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Продукты'].set_column(col_idx, col_idx, column_length)
        
        writer.close()


if __name__ == '__main__':
    cURL = """curl 'https://catalog.wb.ru/catalog/electronic22/v2/catalog?appType=1&curr=rub&dest=-1257786&sort=pricedown&spp=30&subject=515' \
  -H 'Accept: */*' \
  -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Origin: https://www.wildberries.ru' \
  -H 'Referer: https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0' \
  -H 'sec-ch-ua: "Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --compressed"""
    test = Parser(cURL=cURL)
    test.parse(pages_count=50)

