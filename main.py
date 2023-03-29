import hashlib
import telebot
import sqlite as s
import os
import uuid
from sqlite import conn, cursor

bot = telebot.TeleBot("5989044980:AAFXuN6EZcNDGhSKNgrNuPgdEVqp76yoUTs")


def key(password, salt):
    keyF = hashlib.sha256((password + salt).encode()).hexdigest()
    return keyF
def logpass(password, salt, keyp):
    if password == key(keyp, salt):
        return True
    else:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я тестовый бот ввода пароля")

@bot.message_handler(commands=['reg'])
def check(message):
    user_id = message.from_user.id
    if s.getTrue(user_id=user_id) is False:
        mes = bot.send_message(message.chat.id, text='Введите желаемый пароль')
        bot.register_next_step_handler(mes, reg)
    else:
        bot.send_message(message.chat.id, text='Вы зарегистрированы ')
        if s.getName(conn=conn, user_id=user_id) is None:
            mes = bot.send_message(message.chat.id, text='Но вы не ввели пароль. \n Введите желаемый пароль')
            bot.register_next_step_handler(mes, pass_set)
def reg(message):
    user_id = message.from_user.id
    username = message.from_user.username
    salt = uuid.uuid4().hex
    password = message.text
    passw = key(password, salt)
    s.db_table_val(user_id=user_id, username=username, passw=passw, salt=salt)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text='Вы зарегистрированы ')
def pass_set(message):
    user_id = message.from_user.id
    username = message.from_user.username
    salt = uuid.uuid4().hex
    password = message.text
    passw = key(password, salt)
    s.db_table_ed(passw=passw, user_id=user_id)
    s.db_table_ed2(salt=salt, user_id=user_id)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text='Вы установили пароль')


@bot.message_handler(commands=['login'])
def login(message):
    user_id = message.from_user.id
    username = message.from_user.username
    mes = bot.send_message(message.chat.id, text='Введите пароль, пожалуйста')
    bot.register_next_step_handler(mes, get_password)
def get_password(message):
    user_id = message.from_user.id
    username = message.from_user.username
    passw = s.getName(conn=conn, user_id=user_id)
    salt = s.getSalt(conn=conn, user_id=user_id)
    result = logpass(passw, salt, message.text)
    if result is True:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Пароль верный!")
    else:
        mes = bot.send_message(message.chat.id, text='Неверный пароль, попробуйте еще раз')
        bot.register_next_step_handler(mes, get_password)


bot.infinity_polling()