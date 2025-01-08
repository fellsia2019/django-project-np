# Pet project

Названия нет, описания тоже)
Это обычный пет проект для обретения дополнительного опыта и общупывание всякого и разного
Фронт для этого проекта - https://github.com/fellsia2019/nuxt3-project-np

## Установка

Следуйте данным инструкциям, чтобы развернуть копию проекта на вашей локальной машине для разработки и тестирования.

### Требования

- Python 3.9x
- Django 5.x или выше


### Клонирование репозитория

Сначала клонируйте репозиторий на свою локальную машину:

```bash
git clone git@github.com:fellsia2019/django-project-np.git
```

### Установка зависимостей

Рекомендуется создать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Для Unix или MacOS
venv\Scripts\activate     # Для Windows
```

Установите необходимые библиотеки:

```bash
pip install -r requirements.txt
```

### Настройка базы данных

1. Создайте базу данных и пользователя (например, PostgreSQL, SQLite и т.д.).
2. Настройте подключение к базе данных в `settings.py` вашего проекта.
3. Примените миграции:

```bash
python manage.py migrate
```

### Запуск сервера

Запустите локальный сервер:

```bash
python manage.py runserver
```

Теперь вы можете открыть [http://127.0.0.1:8000](http://127.0.0.1:8000) в вашем браузере.

## Тестирование

Инструкции по запуску тестов:

```bash
python manage.py test
```
