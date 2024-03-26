# Wildberries-parser
Парсит данные с каталога с сайта https://www.wildberries.ru о товарах такие как: артикул, id поставщика, id продавца, цена, кол-во штук в наличии, рейтинг продавца и т.п.
Получаем файл .xlsx на подобие данного: 

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/8ec92a4c-acfe-4ebb-8cd8-83351d3de346)

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/4ebf677b-4d11-43e5-bdc8-801505fe11aa)


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

### 1) Открываем Wildberries в интересующем нам каталоге с уже применёнными нами фильтрами, копируем ссылку:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/a5563ce0-b658-4573-8e40-cdf48801af18)

### 2) Открываем WildberriesParser.py, и вставляем скопированную ссылку в переменную url:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/f128c1f6-37c3-4ac1-8de2-eae53bc60ffd)

Код примера если нужно)
```html
url = 'сюда свой url'
start = time.time()

test = Parser(url=url)
test.parse(pages_count=50)

end = time.time()
print(f"Парсинг занял {round(end - start,4)} с")
```


### 3) Запускаем код, ждём пока он выполнится:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/cf840dcc-57de-4bba-8210-9139b82ada6b)

### 4) В директории куда вы всё скачали, ищем файл wb_data.xlsx

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/f45a5b28-138e-4968-b2e0-96220e2f41c7)

### 5) Наслаждаемся проделанной работой

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/916f9b16-cd52-4688-87c2-d9a891955a4b)


    






