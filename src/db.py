import os
from pymongo import AsyncMongoClient
from beanie import init_beanie
from src.models import NLPResult
from dotenv import load_dotenv


def get_env_config() -> tuple[str, str, str, str]:
    """
    Получение переменных из .env конфига
    """
    load_dotenv()

    client_username = os.environ.get('MONGO_USERNAME')
    client_password = os.environ.get('MONGO_PASSWORD')
    mongodb_port = os.environ.get('MONGO_PORT')
    mongodb_name = os.environ.get('MONGO_DB_NAME')

    required_variables = {
        "MONGO_USERNAME": client_username,
        "MONGO_PASSWORD": client_password,
        "MONGO_PORT": mongodb_port,
        "MONGO_DB_NAME": mongodb_name
    }
    for variable, value in required_variables.items():
        if value is None:
            raise ValueError(f'Значение для {variable} не установлено в .env файле')
        
    return client_username, client_password, mongodb_port, mongodb_name # type: ignore переменные уже проверены на отсутствие значения


async def init_db():
    """
    Подключение к базе данных
    """
    client_username, client_password, mongodb_port, mongodb_name= get_env_config()

    # создание ссылки подключения к БД на основе .env конфигурации. Ссылка имеет следующий формат: mongodb://имя-пользователя:пароль-пользователя@хост:порт
    db_connection_link = f'mongodb://{client_username}:{client_password}@localhost:{mongodb_port}/'
    # инициализация клиента для взаимодействия с mongodb
    client = AsyncMongoClient(db_connection_link)
    # инициализация Beanie ORM (Object-Relational Mapping), чтобы можно было создавать модели и документы
    await init_beanie(
        database=client[mongodb_name], # указываем название базы для данных, берем из .env MONGO_DB_NAME
        document_models=[NLPResult] # здесь нужно передать все модели, которые могут быть в базе данных
    )

    print(f"✅ Успешное подключение к базе данных! MongoDB доступна по ссылке: {db_connection_link}")