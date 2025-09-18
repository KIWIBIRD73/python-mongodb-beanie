from typing import List, Literal
from datetime import datetime
from beanie import Document
from pydantic import BaseModel

# Подмодели
class Entity(BaseModel):
    text: str
    label: str

class PosTag(BaseModel):
    text: str
    pos: str

class Preprocessing(BaseModel):
    tokens_by_word: List[str]
    tokens_by_symbol: List[str]
    lowercased: str
    no_punct: str
    alnum_keep: str

# Основной документ
class NLPResult(Document):
    raw_text: str
    language: Literal['en', 'ru']
    preprocessing: Preprocessing
    lemmas: List[str]
    entities: List[Entity]
    pos_tags: List[PosTag]
    created_at: datetime

    class Settings:
        name = "nlp_results"   # имя коллекции


"""
В итоге описана структура для следующего документа:
{
  "_id": ObjectId("...") // генерируется автоматически
  "raw_text": String
  "language": String // в БД строка, но в коде еще жестче фиксируем типизацию с помощью указания типа Literal['en', 'ru']
  "preprocessing": {
    "tokens_by_word": Array // массив из строк
    "tokens_by_symbol": Array // массив из строк
    "lowercased": String
    "no_punct": String
    "alnum_keep": String
  },
  "lemmas": Array, // массив из строк
  "entities": [
    {"text": String, "label": String}
  ],
  "pos_tags": [
    {"text": String, "label": String}
  ],
  "created_at": DateTime
}

Таким образом в коде фиксируем структуру моделей и документов для MongoDb
"""
