import random
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions.db_functions import get_quiz_index, update_quiz_index
from read_questions import quiz_data

def generate_options_keyboard(answer_options, correct_option):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()
    
    answer_options_shuffled = random.sample(answer_options, len(answer_options))

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options_shuffled:
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            # text=option,
            text=option['answer'],
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'

            callback_data=f"button_{option['id']}_{correct_option}")
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(quiz_data[current_question_index]['options'], quiz_data[current_question_index]['correct_option'])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)
            
async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    current_points = 0
    await update_quiz_index(user_id, user_name, current_question_index, current_points)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)
