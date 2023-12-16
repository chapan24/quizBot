from random import randint

welcome_stickers = [
    'CAACAgIAAxkBAAEK7F5lcxfSs7bYy8wSjKJFA3CHQdOyWwAC4QADUomRIznBNrZHX5TMMwQ',
    'CAACAgIAAxkBAAEK7FxlcxeyZ0Px4eAsH2vI5-HKM6s51wACaTEAAnzk-UpTbk5qf7hyeDME',
    'CAACAgIAAxkBAAEK7GJlcxgUtxl4XaZi1uDmMThA5miwGQACGTYAAszDAAFIF2Mh4zqykr4zBA'
]

like_stickers = [
    'CAACAgIAAxkBAAEK7FRlcxbkBYvV4ypNZ5UNssFAlkR2mAAC_gADVp29CtoEYTAu-df_MwQ',
    'CAACAgIAAxkBAAEK7FZlcxcQljf4_i2hxLi5uuN3QGXlbwAC_TQAAg2kiEll1yZExqlHDTME',
    'CAACAgIAAxkBAAEK7FplcxdpnFk_qFQVbV_Ll1ZZXKSz9QACRgADUomRI_j-5eQK1QodMwQ'
]


def send_hi_sticker():
    sticker = welcome_stickers[randint(0, 2)]

    return sticker


def send_like_sticker():
    sticker = like_stickers[randint(0, 2)]

    return sticker


def send_phrases_true():
    phrases = ['Несомненно точно!', 'Верно!', 'Так держать!',
               'Абсолютно верно', 'Вы правы!']
    phrase = phrases[randint(0, len(phrases) - 1)]

    return phrase


def send_phrases_false():
    phrases = ['Не совсем...', 'А если подумать...', 'Вы не правы.',
               'Подумайте получше']
    phrase = phrases[randint(0, len(phrases) - 1)]

    return phrase
