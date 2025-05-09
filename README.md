# Парсер стены группы ВК

### **Case**

 В одной из групп, на которые я подписан, довольно много содержательных постов. А Вконтакте - нууу, Вконтакте.

### How-to

1) Создать своё приложение для получения [*сервисного ключа доступа*](https://dev.vk.com/ru/api/access-token/getting-started#Сервисный%20ключ%20доступа)

    Вот [тут](https://vk.com/apps?act=manage) можно создать своё приложение.
2) С помощью [`wall.get`](https://dev.vk.com/ru/method/wall.get) можно уже парсить данные (запросы можно делать прямо по ссылке, в целом для малого количества постов можно обойтись и без кода)
3) `pip install -r requirements.txt`
4) `config_example.json` переименовать в `config.json`

    1) Написать id нужной группы в поле `owner_id` (nb! это отрицательное число).
    2) В поле `number_of_posts_to_parse` обозначить, сколько постов необходимо спарсить (или оставить 0, если требуются все)

5) Создать файл `.env` и вписать туда `ACCESS_TOKEN=<ваш сервисный ключ доступа>`
6) Запустить `src/main.py` и ждать результат в `results/all.md`

    Обратите внимание, лично мне важно удобство чтения актуальных постов, поэтому запись файл происходит "в обратном порядке" (то есть более поздние посты записываются "выше" в файле, в частности самый первый пост находится в самом начале файла)

### Extra

В коде можно заметить функцию `parse_only_sunday_posts`. Дело в том, что помимо абсолютно всех постов группы, мне потребовались посты по весьма специфичному правилу: только те, что были выложены после 18 сентября 2016 года, и только по воскресеньям. В соответствии с этими правилами вышеуказанная функция парсит всё, фильтрует нужное и нумерует+записывает посты в их прямом порядке (то есть самый старый пост имеет номер 0, находится в начале файла).
