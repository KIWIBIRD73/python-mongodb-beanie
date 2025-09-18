import os
from pymongo import MongoClient
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

    db_connection_link = f'mongodb://{client_username}:{client_password}@localhost:{mongodb_port}/'
    client = AsyncMongoClient(db_connection_link)
    await init_beanie(database=client[mongodb_name], document_models=[NLPResult])

    print(f"✅ Успешное подключение к базе данных! MongoDB доступна по ссылке: {db_connection_link}")