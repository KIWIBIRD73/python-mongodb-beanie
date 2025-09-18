# MongoDB Tokenizer & NLP Analyzer

## 📌 Описание проекта

Проект предназначен для анализа текста на естественном языке с помощью библиотеки **spaсy**.
Выполняется следующий NLP анализ:

* Токенизация текста по словам и символам.
* Приведение текста к нижнему регистру.
* Очистка текста от пунктуации (полностью или частично).
* Лемматизация текста.
* Извлечение именованных сущностей (NER).
* Определение частей речи (POS).

Результаты анализа сохраняются в **MongoDB** через **Beanie** с полной валидацией документа.

## 📌 Структура проекта
```
└── 📁mongodb-tokenizer
    └── 📁.venv             <- Виртуальное окружение
    └── 📁assets            <- Папка со скриншотами для README.md
    └── 📁data              <- Дамп базы данных из Docker container (появится после запуска Docker)
    └── 📁src               <- Папка с ресурсами проекта
        ├── db.py           <- Скрипт с функциями для подключения к БД
        ├── main.py         <- Точка запуска проекта
        ├── models.py       <- Описание моделей (коллекций) для mongodb
        ├── nlp.py          <- Скрипты для nlp обработки
    ├── .env                <- Конфигурация проекта
    ├── .env.example        <- Пример того как примерно должен выглядеть конфиг (.env)
    ├── .gitignore          <- Файлы и папки, которые не нужно сохранять в git
    ├── docker-compose.yml  <- Конфигурация запуска MongoDB Docker образа
    ├── LICENSE             <- Фаил лицензии, отображается на github, указывает, что проект в свободном доступе (его можно копировать)
    ├── poetry.lock         <- Зафиксированные зависимости для Poetry
    ├── pyproject.toml      <- Описание python проекта
    ├── README.md           <- Фаил с описанием проекта
    ├── requirements.txt    <- Зависимости, необходимые для запуска проекта
    └── SECURITY.md         <- Информация о поддерживаемых версиях проекта, сообщает что делать при нахождении ошибки в проекте, отображается на github
```

---

## 🖼 Пример работы проекта

### Ввод текста:

```bash
Введите предложение для NLP анализа: Владимир Путин посетил Москву в январе 2023 года.
Введите язык текста ('ru' или 'en'): ru
```

### Вывод в консоли:

```bash
✅ Успешное подключение к базе данных! MongoDB доступна по ссылке: mongodb://root:***@localhost:27017/
🚀 Запуск NLP анализа...
⏳ Препроцессинг...
⏳ NLP анализ...
⏳ Сохранение записи в базу данных...
✅ NLP анализ сохранён в базу данных!
💾 ID сохраненного документа: 68cb57810a81be51aa1b6f75
```

### Сохранённый документ в MongoDB:
<div align="center">
  <img src="./assets/screenshot1.jpeg" alt="Application Interface" style="border-radius: 8px;" />
</div>
 
JSON:
```json
{
  "_id": "ObjectId("650f6c3b0e2f4b1fabc12345")",
  "raw_text": "Владимир Путин посетил Москву в январе 2023 года.",
  "language": "ru",
  "preprocessing": {
    "tokens_by_word": ["Владимир", "Путин", "посетил", "Москву", "в", "январе", "2023", "года."],
    "tokens_by_symbol": ["В","л","а","д","и","м","и","р","..."],
    "lowercased": "владимир путин посетил москву в январе 2023 года.",
    "no_punct": "Владимир Путин посетил Москву в январе 2023 года",
    "alnum_keep": "Владимир Путин посетил Москву в январе 2023 года."
  },
  "lemmas": ["Владимир", "Путин", "посетить", "Москва", "в", "январь", "2023", "год"],
  "entities": [{"text": "Владимир Путин", "label": "PER"}, {"text": "Москву", "label": "LOC"}, {"text": "январе 2023", "label": "DATE"}],
  "pos_tags": [{"text": "Владимир", "pos": "PROPN"}, {"text": "Путин", "pos": "PROPN"}, "..."],
  "created_at": "2025-09-18T00:12:34.567Z"
}
```

---

## 🛠 Использованные инструменты

* **VSCode** – редактор кода
* **Python** – язык разработки
* **Poetry** – менеджер зависимостей и виртуальных сред
* **Docker & Docker Compose** – для запуска MongoDB
* **MongoDB Compass** – графический интерфейс для работы с MongoDB
* **Beanie** – ODM для работы с MongoDB

---

## ⚡ Необходимые инструменты для запуска проекта

| Инструмент             | Ссылка                                                                                                                                                   |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| VS Code                | [VS Code Download](https://code.visualstudio.com/download)                                                                                               |
| Python >= 3.12, < 3.14 | [Python Download](https://www.python.org/downloads/)                                                                                                     |
| Poetry                 | [Poetry Download](https://python-poetry.org/docs/#installation)                                                                                          |
| Docker                 | [Docker Download](https://docs.docker.com/engine/install/)                                                                                               |
| Docker Compose         | [Docker Compose Download](https://docs.docker.com/compose/install/) PS: В последних версиях Docker, `docker compose` уже доступен после установки Docker |
| MongoDB Compass        | [MongoDB Compass Download](https://github.com/mongodb-js/compass/releases)                                                                               |

---

## 🔧 Переменные окружения (`.env`)

| Переменная       | Описание                                          | Пример значения |
|------------------|---------------------------------------------------|-----------------|
| `MONGO_USERNAME` | Имя пользователя для подключения к MongoDB        | `root`          |
| `MONGO_PASSWORD` | Пароль пользователя для MongoDB                   | `example`       |
| `MONGO_PORT`     | Порт MongoDB                                      | `27017`         |
| `MONGO_DB_NAME`  | Имя базы данных, куда будут сохраняться документы | `nlp_db`        |

> Создайте файл `.env` на основе `.env.example` и заполните все значения.

---

## 🚀 Запуск MongoDB через Docker Compose

### Поднять контейнер:

```bash
docker compose up --build -d
```

### Остановить контейнер:
Для завершения работы контейнера по окончанию работы с проектом

```bash
docker compose down
```

---

## 🏃 Запуск проекта
1. **Создайте виртуальное окружение**. Нужно для изолированной работы приложения и установки зависимостей
    - windows
      ```bash
      python -m venv .venv
      ```
    - macos/linux
      ```bash
      python3 -m venv .venv
      ```
2. **Активируйте виртуальное окружение**
    - windows
      ```bash
      .venv\Scripts\activate
      ```
    - macos/linux
      ```bash
      source .venv/bin/activate
      ```
3. **Установите зависимости** (windows/macos/linux)
    - Если работа через Python
      ```bash
      pip install -r requirements.txt
      ```
    - Если работа через Poetry
      ```bash
      poetry install 
      ```
4. **Запуск приложения** (windows/macos/linux)
    - Если работа через Python
      ```bash
      python -m src.main
      ```
    - Если работа через Poetry
      ```bash
      poetry run app
      ```

---

## ⚠ Возможные ошибки и их исправление

| Ошибка                               | Причина                        | Решение                                                 |
|--------------------------------------|--------------------------------|---------------------------------------------------------|
| `docker daemon not found`            | Docker не запущен              | Запустите Docker Desktop                                |
| `docker compose: команда не найдена` | Используется старая версия     | Попробуйте команду `docker-compose` или обновите Docker |
| `invalid python version`             | Версия Python не соответствует | Установить Python >= 3.10                               |

---

## 🔗 Полезные ссылки
* [Конфигурация VS Code для работы с Python](https://www.youtube.com/watch?v=D2cwvpJSBX4)
* [Объяснение концептов Python, которые использовались при написании проекта](https://www.youtube.com/watch?v=Gx5qb1uHss4)
* [Документация Beanie](https://beanie-odm.dev/getting-started/)
* [MongoDB Compass Вщцтдщфв](https://github.com/mongodb-js/compass/releases)
* [Подключение к базе MongoDB в Compass](https://www.mongodb.com/docs/compass/current/connect/)
* [Запуск проекта через Poetry](https://python-poetry.org/docs/cli/#run)

---
