from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cmds = '''
<b>Info</b> - информация о разботчике
<b>Literature</b> - источники информации
<b>Quiz</b> - начать викторину

'''


def get_ikb_return():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Main menu', callback_data='help')]
    ])

    return ikb


def get_ikb_help():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Help', callback_data='help')]
    ])

    return ikb


def get_ikb_cmds():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Info', callback_data='info'),
         InlineKeyboardButton('Literature', callback_data='lit')],
        [InlineKeyboardButton('Quiz', callback_data='quiz')]
    ])

    return ikb


def send_literature():
    ikb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton('Link', url='https://detskiychas.ru/school/pushkin/victorina_biografiya_pushkina'
                                          '/?ysclid=loswj6m18g215772164')],
        [InlineKeyboardButton('←', callback_data='back')]
    ])

    return ikb


def send_link_creator():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Creator', url='tg://resolve?domain=sfhghitfhi')],
        [InlineKeyboardButton('←', callback_data='back')]
    ])

    return ikb


def get_ikb_results():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Result', callback_data='result')]
    ])

    return ikb
