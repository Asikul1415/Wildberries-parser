# Wildberries-parser
Парсит данные с каталога с сайта https://www.wildberries.ru о товарах такие как: артикул, id поставщика, id продавца, цена, кол-во штук в наличии, рейтинг продавца и т.п
Получаем файл .xlsx на подобие данного: 

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/8ec92a4c-acfe-4ebb-8cd8-83351d3de346)

Необходимые  библиотеки для работы библиотеки: requests, xlsxwriter:
---

```html
  pip install requests
```

```html
  pip install xlsxwriter
```


Как работать с этим
====================
Вот пример работы с данным парсером. 

### 1) Открываем Wildberries в интересующем нам каталоге с уже применёнными нами фильтрами:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/1ac7c50c-1536-4a52-8606-57ec1aa7b251)

### 2) Открываем инструменты разработчка (код элемента):

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/cf90ffb2-573f-442e-b21a-36e5ac4d95e7)

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/da6d28b6-c17a-4d75-af07-3b0fb98996a4)

### 3) Переходим на вкладку Network и выбираем из фильтров Fetch/XHR:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/8871c218-eedd-42d2-8e7b-6937c4c7529d)

### 4) Перезагружаем страницу и смотрим что нам пришло:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/ed1131c1-b971-40bd-8b06-b54c8578263e)

### 5) Ищем подобный запрос и тыкаем по нему правой кнопкой:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/5200fe7a-de87-40a7-9748-cda0847cf1e9)

### 6) Выбираем копировать как cURL (bash):

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/0ee6e8cb-893d-4e21-a504-de2b488b901a)

### 7) Открываем редактор кода и в нём WildberriesParser.py

### 8) Пишем без отступа после класса на подобие этого:
     

```html
cURL = """curl 'https://catalog.wb.ru/catalog/men_clothes1/v2/catalog?appType=1&cat=8144&curr=rub&dest=-1257786&fbrand=524&page=1&sort=rate&spp=30&xsubject=216' \
  -H 'Accept: */*' \
  -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Origin: https://www.wildberries.ru' \
  -H 'Referer: https://www.wildberries.ru/catalog/muzhchinam/odezhda/bryuki-i-shorty?sort=rate&page=1&xsubject=216&fbrand=524' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0' \
  -H 'sec-ch-ua: "Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --compressed""" #сюда вставьте скопированный cURL
test = Parser(cURL=cURL)
test.parse(pages_count=50) #в pages_count указываете сколько страниц хотите спарсить, больше 50 нельзя
```

### 9) Запускаете код, ждёте пока выполнится, и затем идёте искать в директорию, куда скачали данные файлы файл wb_data.xlsx.

### 10) Наслаждаетесь проделанной работой
    






