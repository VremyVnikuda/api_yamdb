# YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.<br /><br />
API проекта YaMDb собирает отзывы пользователей на произведения.<br />

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).<br /><br /> 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.<br /><br />
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.<br /><br />
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
### Технологии:
Python, Django, DRF, JWT
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git git@github.com:CrockoMan/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
Возможно загрузить предварительно подготовленные cvs файлы с данными в БД
```
python3 manage.py load_csv
```

Запустить проект:

```
python3 manage.py runserver
```
### Алгоритм регистрации пользователей<br />
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт http://127.0.0.1:8000/api/v1/auth/signup/.<br />
```
POST
{
  "email": "user@example.com",
  "username": "string"
}

Response
{
  "email": "string",
  "username": "string"
}
```
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.<br />

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт http://127.0.0.1:8000/api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).<br />
```
POST
{
  "username": "string",
  "confirmation_code": "string"
}

Response
{
  "token": "string"
}
```
При желании пользователь отправляет PATCH-запрос на эндпоинт http://127.0.0.1:8000/api/v1/users/me/ и заполняет поля в своём профайле<br /><br />

### Категории (типы) произведений
<http://127.0.0.1:8000/api/v1/categories/><br />
```
GET
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
```
POST
{
  "name": "string",
  "slug": "string"
}

Response
{
  "name": "string",
  "slug": "string"
}
```
```
DEL
<http://127.0.0.1:8000/api/v1/categories/{slug}/><br />
```
### Жанры произведений
<http://127.0.0.1:8000/api/v1/genres/><br />
```
GET
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
```
POST
{
  "name": "string",
  "slug": "string"
}

Response
{
  "name": "string",
  "slug": "string"
}
```
```
DEL
<http://127.0.0.1:8000/api/v1/genres/{slug}/><br />
```
### Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).<br />
Получить список всех объектов<br />
<http://127.0.0.1:8000/api/v1/titles/><br/>
```
GET
Response
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
Добавить новое произведение. При добавлении нового произведения требуется указать уже существующие категорию и жанр.<br />
<http://127.0.0.1:8000/api/v1/titles/><br/>
```
POST
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}

Response
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Работа с произведением<br />
<http://127.0.0.1:8000/api/v1/titles/{titles_id}/><br/>

Получение информации о произведении<br />
```
GET

Response
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Частичное обновление информации о произведении<br />
```
PATCH
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}

Response
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Удаление произведения<br />
```
DEL

```
### Отзывы<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/<br />

Получение списка всех отзывов<br />
```
GET

Respone
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
Добавить новый отзыв.<br />
```
POST
{
  "text": "string",
  "score": 1
}

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Получить отзыв по id для указанного произведения<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/<br />
```
GET

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частично обновить отзыв по id<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/<br />
```
PATCH
{
  "text": "string",
  "score": 1
}

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление отзыва по id<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/<br />
```
DEL
```
### Комментарии к отзывам<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/<br />
```
GET

Response
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
Добавление комментария к отзыву<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/<br />
```
POST
{
  "text": "string"
}

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Получить комментарий для отзыва по id<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/<br />
```
GET

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частично обновить комментарий к отзыву по id<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/<br />
```
PATCH
{
  "text": "string"
}

Response
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удалить комментарий к отзыву по id<br />
<http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/<br />
```
DELETE
```
### Работа с пользователями<br />
<http://127.0.0.1:8000/api/v1/users/><br /><br />
Получить список всех пользователей.<br />
```
GET

Response
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```
Добавить нового пользователя<br />
<http://127.0.0.1:8000/api/v1/users/><br />
```
POST
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}

Response
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Получить пользователя по username.<br />
<http://127.0.0.1:8000/api/v1/users/{username}/><br />
```
GET

Response
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Изменить данные пользователя по username.<br />
<http://127.0.0.1:8000/api/v1/users/{username}/><br />
```
PATCH
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}

Response
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Удалить пользователя по username<br />
<http://127.0.0.1:8000/api/v1/users/{username}/><br />
```
DELETE
```
Изменить данные своей учетной записи<br />
<http://127.0.0.1:8000/api/v1/users/{username}/><br />
```
PATCH
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}

Response
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Документация доступна по адресу <http://127.0.0.1:8000/redoc/><br /><br />
Автор: К.Гурашкин [А.Копнин](<https://github.com/VremyVnikuda>) М.Плевин
