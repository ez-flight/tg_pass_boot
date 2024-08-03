import telebot
import os
import xlrd #библиотка чтения экселевских файлов
import random #рандом обязательно
from dotenv import load_dotenv
from telebot import types
from os import urandom
from base64 import b64encode
token = os.getenv('TOKEN')

bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])

def generate_password(length=8):
    if not isinstance(length, int) or length < 8:
        raise ValueError("временный пароль должен иметь положительную длину")

    chars = "!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(chars[c % len(chars)] for c in urandom(length))
#    chars = chars + chars.lower()
#    return "".join(chars[ord(str(c)) % len(chars)] for c in b64encode(urandom(32)).decode('utf-8'))

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("? Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "? Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")
    elif(message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Из файла?")
        btn2 = types.KeyboardButton("Пароль?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif(message.text == "Из файла?"):
        #достаём циататы из ворда
        rb = xlrd.open_workbook('base.xls', formatting_info=True)
        sheet = rb.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            rand = int(random.randint(0,rownum))
            row = sheet.row_values(rand)
        bot.send_message(message.chat.id, row)
    
    elif message.text == "Пароль?":
        texts = generate_password()
        bot.send_message(message.chat.id, texts)
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("? Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

bot.polling(none_stop=True)