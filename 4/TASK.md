# Запросы

В этом упражнении вы будете работать с базой данных, используя SQLAlchemy для выполнения запросов. Ваша задача — создать несколько функций для извлечения данных из таблицы `movies`.

Таблица `movies` имеет следующую структуру:
- `id` — идентификатор фильма, первичный ключ;
- `title` — название фильма;
- `director` — режиссёр фильма;
- `release_date` — дата выпуска фильма;
- `duration` — длительность фильма в минутах;
- `genre` — жанр фильма;
- `rating` — рейтинг фильма.

## src/solution.py

Вам нужно реализовать три функции, которые будут выполнять запросы к базе данных:

- `get_all_movies(session)` — возвращает список всех фильмов, каждый фильм представлен в виде строки формата:  `"The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3"`
- `get_movies_by_director(session, director_name)` — возвращает список фильмов указанного режиссёра `director_name`. Каждая строка фильма должна быть представлена в формате из функции `get_all_movies`. Список должен быть отсортирован по дате выпуска фильмов.
- `get_top_rated_movies(session, n)` — возвращает список из n фильмов с наивысшим рейтингом, отсортированных по убыванию рейтинга. Формат результата должен совпадать с форматом из функции `get_all_movies`.