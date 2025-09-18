import asyncio
from datetime import datetime
from typing import Literal
from src.db import init_db
from src.models import NLPResult, Preprocessing, Entity, PosTag
from src.nlp import (
    tokenize,
    to_lower_text,
    remove_punctuation,
    extract_lemmas,
    extract_entities,
    extract_pos
)

def get_input_sentence() -> str:
    """
    Получение ввода предложения для NLP обработки из терминала пользователя
    
    :return: Введенное пользователем предложение
    :rtype: str
    """
    sentence = input('Введите предложение для NLP анализа: ')
    if not sentence.strip():
        raise ValueError('Предложение не было введено')
    return sentence.strip()


def get_language() -> Literal['ru', 'en']:
    """
    Получение ввода языка на котором будет проводиться NLP обработка
    
    :return: Локаль для введенного предложения `ru` или `en`
    :rtype: Literal['ru', 'en']
    """
    lang = input("Введите язык текста ('ru' или 'en'): ").strip().lower()

    # убеждаемся, что передана одно из указанных локалей
    available_locales = ('ru', 'en')
    while lang not in available_locales:
        lang = input("Введите один из предложенных языков ('ru' или 'en'): ").strip().lower()

    return lang


async def analyze_and_save():
    """
    Запуск NLP анализа на основе переданного текста из `get_input_sentence` и локали из `get_language`
    """
    sentence = get_input_sentence()
    language = get_language()

    print('🚀 Запуск NLP анализа...')

    # Препроцессинг
    print('⏳ Препроцессинг...')
    tokens_word = tokenize(sentence, 'word')
    tokens_symbol = tokenize(sentence, 'symbol')
    lowercased = to_lower_text(sentence)
    no_punct = remove_punctuation(sentence, 'no_punct')
    alnum_keep = remove_punctuation(sentence, 'alnum_keep')

    preprocessing = Preprocessing(
        tokens_by_word=tokens_word,
        tokens_by_symbol=tokens_symbol,
        lowercased=lowercased,
        no_punct=no_punct,
        alnum_keep=alnum_keep
    )

    # NLP анализ
    print('⏳ NLP анализ...')
    lemmas = extract_lemmas(sentence, language)
    entities_list = [Entity(text=text, label=label) for text, label in extract_entities(sentence, language)]
    pos_tags_list = [PosTag(text=text, pos=pos) for text, pos in extract_pos(sentence, language)]

    # Создание итогового документа в mongoDB в в коллекцию nlp_result
    doc = NLPResult(
        raw_text=sentence,
        language=language,
        preprocessing=preprocessing,
        lemmas=lemmas,
        entities=entities_list,
        pos_tags=pos_tags_list,
        created_at=datetime.utcnow()
    )

    print('⏳ Сохранение записи в базу данных...')
    # обязательно нужно сохранить созданный документ
    await doc.insert()
    print("✅ NLP анализ сохранён в базу данных!")
    print(f"💾 ID сохраненного документа: {doc.id}")


async def main():
    """
    Основная функция, которая запускает проект
    """
    await init_db()
    await analyze_and_save()

# Точка входа в приложение
# Для запуска через Poetry
def run():
    asyncio.run(main())

# Для запуска через Python
if __name__ == "__main__":
    run()