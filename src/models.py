from typing import List, Literal
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field

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
