
from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from prettytable import PrettyTable

from functions.db_functions import get_quiz_index, update_quiz_index, get_quiz_points, get_quiz_players_stats
from functions.utils_functions import new_quiz, get_question
from read_questions import quiz_data

router = Router()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команды /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)

@router.callback_query(F.data.startswith("button_"))
async def handle_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

     # Получение текущего вопроса для данного пользователя 
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_points = await get_quiz_points(callback.from_user.id)
    print('current points =', current_points)

    options = quiz_data[current_question_index]['options']
    option_index = int(callback.data.split('_')[1])
    correct_option_index = int(callback.data.split('_')[2])
   

    await callback.message.answer(f"Ваш ответ: {options[option_index]['answer']}")

    if option_index == correct_option_index:
        await callback.message.answer("Верно!")
        current_points += 1
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {options[correct_option_index]['answer']}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, callback.from_user.first_name, current_question_index, current_points)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Вы ответили на {current_points} вопросов из {len(quiz_data)}")

@router.message(Command('stats'))
async def print_players(message: types.Message):
    items = await get_quiz_players_stats()

    table = PrettyTable()
    
    table.field_names = ['Имя', 'Правильные ответы']
    
    for item in items:
        table.add_row([item[1], item[3]])
    
    response_t = '```\n{}```'.format(table.get_string())

    await message.answer(response_t, parse_mode='Markdown')