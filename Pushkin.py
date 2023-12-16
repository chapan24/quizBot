import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from token_ import TOKEN_API

from parse import get_question, get_answer, reset
from says_phrases import send_like_sticker, send_hi_sticker
from keyboards import (get_ikb_help, get_ikb_cmds, cmds, get_ikb_return,
                       get_ikb_results, send_link_creator, send_literature)

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

count = 0

answers_count = 0


class TasksStatsGroup(StatesGroup):
    question = State()
    answer = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker=send_hi_sticker())
    await message.answer('Привет! Я Квиз-Бот, который составляет и проводит '
                         'викторины по биографии Пушкина и его творчеству!'
                         ' Для того, чтобы узнать, что я умею, нажмите - <b>Help</b>!',
                         reply_markup=get_ikb_help(),
                         parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'help')
async def send_help_cmds(callback: types.CallbackQuery):
    await callback.message.edit_text(f'<b>Список моих команд</b>: {cmds}',
                                     reply_markup=get_ikb_cmds(),
                                     parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back')
async def check_back(callback: types.CallbackQuery):
    await callback.message.edit_text(f'<b>Список моих команд</b>: {cmds}',
                                     reply_markup=get_ikb_cmds(),
                                     parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'info')
async def check_info(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Info</b>\nThe creator - Sergey.',
                                     reply_markup=send_link_creator(),
                                     parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'lit')
async def check_literature(callback: types.CallbackQuery):
    await callback.message.edit_text(f'<b>Literature</b>\nИсточник информации:',
                                     reply_markup=send_literature(),
                                     parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'quiz')
async def check_info_and_question_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('❗')
    await callback.message.answer('Ответы на вопросы должны быть обязательно <b>ПОЛНЫМИ</b>',
                                  parse_mode='HTML')
    await callback.message.answer('Если Вы захотите завершить викторину - /cancel')

    await asyncio.sleep(1.5)

    await callback.message.answer('Вы успешно запустили викторину. Желаю удачи!')
    await callback.bot.send_sticker(callback.from_user.id,
                                    sticker=send_like_sticker())

    await TasksStatsGroup.question.set()
    async with state.proxy() as data:
        data['question'] = get_question()

    await callback.message.answer(data['question'])

    await TasksStatsGroup.next()


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_quiz(message: types.Message, state: FSMContext):
    global count, answers_count
    count = 0
    answers_count = 0
    reset()

    await state.finish()
    await message.reply('Завершаю процесс викторины...')
    await asyncio.sleep(1)
    await message.answer('Вы можете узнать результат, нажав на кнопку <b>Result</b>.',
                         reply_markup=get_ikb_results(),
                         parse_mode='HTML')


@dp.message_handler(state=TasksStatsGroup.answer)
async def check_answer_1(message: types.Message, state: FSMContext):
    global count
    global answers_count

    if count >= 7:
        await state.finish()

        await bot.send_sticker(message.from_user.id,
                               sticker='CAACAgIAAxkBAAEK7-dldaVELefUB-217EnhGKULRhXa-wACdjoAAhT3wUj30QABlITL9QMzBA')
        await message.answer('Вы успешно прошли викторину по биографии и творчеству А.С.Пушкина!')
        await message.answer('Вы можете узнать результат, нажав на кнопку <b>Result</b>.',
                             reply_markup=get_ikb_results(),
                             parse_mode='HTML')

    else:
        count += 1

        if count == 7:
            await message.answer('Последний вопрос!')

        answer = message.text
        async with state.proxy() as data:
            data['answer'] = answer

        if data['answer'].lower() == get_answer():
            answers_count += 1

        await TasksStatsGroup.question.set()

        async with state.proxy() as data:
            data['question'] = get_question()

        await message.answer(data['question'])
        await TasksStatsGroup.next()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'result')
async def callback_result(callback: types.CallbackQuery):
    global answers_count, count

    await callback.message.answer(f'Количество верных ответов: <b>{answers_count}</b>.',
                                  parse_mode='HTML')

    reset()
    answers_count = 0
    count = 0

    await asyncio.sleep(1)

    await callback.message.answer('Чтобы вернуться в главное меню - нажмите <b>Main menu</b>',
                                  reply_markup=get_ikb_return(),
                                  parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
