# Wildberries-parser async
## Разница между обычным парсером и асинхронным:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/8e03236d-b9fe-42fb-8536-8b937fb0fe69)

Асинхронный спарсил это за 14.9 секунд
---

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/009ccb9d-5ee3-46e9-a1df-ccd109d64c0b)

Обычный спарсил этот же каталог за 37.8 секунд
---

### Но теперь про главную проблему асинхронного парсера:

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/7008abf8-3e4c-4eb3-be20-4ea6fd0fe9b2)

Асинхронный спасрил 20513 товаров
---

![image](https://github.com/Asikul1415/Wildberries-parser/assets/83174848/9bafad12-8a14-49be-839f-6061597d8132)

В то время как обычный спарсил все 21729 товаров
---

И это ещё неплохой случай, тут разница всего в 1200 товаров, а бывает что она достигает 2-3 тысяч. Я точно не знаю почему некоторые рабочие страницы сервер WB отдаёт с кодом 200 и пустым json асинхронному, в то время как обычному если он такое и отдаёт, то эта страница пустая и товары уже кончились. Здесь же подобную ошибку можно и на 4 странице поймать из 74. Пробовал ограничивать кол-во запросов в единицу времени путём Semasphore, но разницы нету абсолютно никакой.










