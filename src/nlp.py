import subprocess
from typing import Literal
import re
import spacy
from spacy.language import Language


def ensure_spacy_model(model_name: str):
    """
    Проверяет, есть ли модель spacy, и если нет — устанавливает её через subprocess.
    """
    try:
        spacy.load(model_name)
    except OSError:
        print(f"Модель {model_name} не найдена. Установка...")
        subprocess.run(
            ["python", "-m", "spacy", "download", model_name],
            check=True
        )
        print(f"Модель {model_name} установлена.")

def load_nlp(language: Literal['ru', 'en']) -> Language:
    """
    Возвращает объект nlp для указанного языка с автоматической установкой модели.
    """
    model_map = {
        "ru": "ru_core_news_sm",
        "en": "en_core_web_sm"
    }
    if language not in model_map:
        raise ValueError("Поддерживаются только языки: 'ru' и 'en'")

    model_name = model_map[language]
    ensure_spacy_model(model_name)
    return spacy.load(model_name)


def tokenize(raw_text: str, tokenize_by: Literal['word', 'symbol']) -> list[str]:
  """
  Разбивает переданный текст `raw_text` на токены
  
  :param raw_text: Текст для токенизации
  :type raw_text: str
  :param tokenize_by: Режим работы. `word` - разбиение текста на токены через пробел `symbol` - разбиение текста на отдельные символы
  :type tokenize_by: Literal['word', 'symbol']
  """
  match tokenize_by:
    case 'word':
        return raw_text.split(' ')
    case 'symbol':
        return list(raw_text)
    case _:
        raise ValueError('Unknow tokenize_by value')
     

def to_lower_text(raw_text: str) -> str:
   """
   `raw_text` к нижнему регистру
   
   :param raw_text: Текст на вход
   :type raw_text: str
   """
   return raw_text.lower()


def remove_punctuation(
    raw_text: str,
    clean_mode: Literal['no_punct', 'alnum_keep', 'none'] = 'none'
) -> str:
   """
   Позволяет убрать пунктуацию из переданного текста `raw_text`
   
   :param raw_text: Текст из которого нужно убрать пунктуацию
   :type raw_text: str
   :param clean_mode: Режим работы. `no_punct` - убирает всю пунктуацию `alnum_keep` - Убирает всю пунктуацию кроме чисел `none` - оставить всю пунктуацию
   :type clean_mode: Literal['no_punct', 'alnum_keep', 'none']
   """
   match clean_mode:
        case 'no_punct':
            return re.sub(r'[^\w\s]', '', raw_text)
        case 'alnum_keep':
            return re.sub(r'[^a-zA-Zа-яА-Я0-9\s.,!?]', '', raw_text)
        case 'none':
            return raw_text
        case _:
            raise ValueError("Unknown clean_mode value")
       

def extract_lemmas(raw_text: str, language: Literal['ru', 'en'] = "ru") -> list[str]:
    """
    Лемматизация текста. Перед началом работы установить зависимости: poetry run python -m spacy download ru_core_news_sm
    
    :param raw_text: Текст, который нужно лемматизировать
    :type raw_text: str
    :param language: Язык на котором передан текст
    :type language: Literal['ru', 'en']
    """
    nlp = load_nlp(language)
    doc = nlp(raw_text)

    lemmas: list[str] = []
    for word in doc:
        lemmas.append(word.lemma_)

    return lemmas


def extract_entities(raw_text: str, language: Literal['ru', 'en'] = "ru") -> list[tuple[str, str]]:
    """
    Извлекает именованные сущности из текста с помощью spaCy.
    
    :param text: Входной текст
    :param language: 'en' или 'ru' (по умолчанию 'en')
    :return: список кортежей (сущность, тип)
    """
    nlp = load_nlp(language)
    doc = nlp(raw_text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def extract_pos(text: str, language: Literal['ru', 'en'] = "ru") -> list[tuple[str, str]]:
    """
    Извлекает части речи из текста с помощью spaCy.
    
    :param text: Входной текст
    :param language: 'en' или 'ru' (по умолчанию 'en')
    :return: список кортежей (слово, часть речи)
    """
    
    nlp = load_nlp(language)
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]
