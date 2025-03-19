# Zuzublik Parser Bot

Телеграм-бот для парсинга цен с сайтов и их анализа. Бот принимает Excel-файл с данными сайтов, автоматически получает цены и вычисляет их среднее значение.

📌 Функциональность

📂 Загрузка Excel-файла с перечнем сайтов для парсинга.

🌐 Автоматический парсинг цен с указанных сайтов.

📊 Расчет средней цены по каждому сайту.

🤖 Телеграм-бот с командами для взаимодействия.

## Установка

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:heydolono/zuzublik_parser_bot.git
```
```
cd zuzublik_parser_bot
```

### Настройка переменных окружения:

Переименуйте .env.example в .env и заполните переменные

```
TOKEN=ТОКЕН_БОТА
DATABASE_URL=БАЗА_ДАННЫХ_(sqlite:///database.db)
DOWNLOADS_DIR=ДИРЕКТОРИЯ_ЗАГРУЗОК(downloads)
```

### Создаем виртуальное окружение и устанавливаем зависимости:
```
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

### Создаем миграции базы данных:

```
alembic revision --autogenerate -m "init migrate"
```
```
alembic upgrade head
```

## Использование

### Консольные команды

### Запускаем бота

```
python bot.py
```

### Запускаем парсер

```
python parser.py
```

### Использование бота

1. Запусти бота с командой /start

2. Отправь Excel-файл с колонками title, url, xpath

3. Нажми кнопку "Спарсить" для сбора данных и вывода средней цены

## Разработчик
- [Максим Колесников](https://github.com/heydolono)
- [Резюме](https://career.habr.com/heydolono)