"""
Handlers for all commands
"""
import os
import math
import random
from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, KeyboardButton
import classes
import constants

USERS_COMMENT = {}
USERS_REGISTRATION = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Реєстрація', 'Подивитись учасників'],
                                        ['Залишити коментар', 'Вихідний код'],
                                        ['Головне меню']],
                                       resize_keyboard=True)
MARK, CONTACT = range(2)
REGISTRATION_END = range(1)


# MAIN MENU
def start(bot, update):
    update.message.reply_text('Привіт!\n'
                              'Я чат-бот, який буде проводити гру Таємний Санта\n\n'
                              'Тут ви можете зареєструватися щоб брати участь у грі\n'
                              'Також можно полазити по меню тут багато цікавого  👌',
                              reply_markup=MAIN_MENU_MARKUP)


def main_menu(bot, update):
    update.message.reply_text('Головне меню',
                              reply_markup=MAIN_MENU_MARKUP)


# SOURCE
def source(bot, update):
    update.message.reply_text('Відкритий вихідний код\n'
                              'Це ж прямо <b>GNU</b> !!11!\n'
                              'https://github.com/orlovw/animkabot',
                              reply_markup=MAIN_MENU_MARKUP,
                              parse_mode='HTML')


# COMMENT
def comment(bot, update):
    user = update.message.from_user
    new_user = classes.CommentUser(username=user.username, first_name=user.first_name, last_name=user.last_name)
    chat_id = update.message.chat_id
    USERS_COMMENT.update({chat_id: new_user})

    markup = ReplyKeyboardMarkup([['/cancel']], resize_keyboard=True)
    update.message.reply_text('Коментар щодо виконання бота\n'
                              'Я все прочитаю і відповім на ваші питання\n\nКоитки'
                              '\n\n /cancel для скасування команди',
                              quote=True, parse_mode='HTML', reply_markup=markup)
    return MARK


def comment_mark(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    user = USERS_COMMENT.get(chat_id)
    user.add_comment(text)
    update.message.reply_text('Дякую за коментар\n\n'
                              'Яку б оціночку цьому боту ви б поставили по 12-бальній системі?\n',
                              quote=True)
    return CONTACT


def comment_contact(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        text = int(text)
    except ValueError:
        update.message.reply_text('Оціночка це число (наприклад 1,2,3)\n'
                                  'Арабськими цифрами(число натуральне від 0 до 12)')
        return CONTACT

    if text > 12:
        update.message.reply_text('Число більше 12\nСпробуйте ще раз)')
        return CONTACT

    if text < 0:
        update.message.reply_text('Число менше 0\nСпробуйте ще раз)')
        return CONTACT

    user = USERS_COMMENT.get(chat_id)
    user.add_mark(text)
    #239062390 - @orlow
    bot.sendMessage(chat_id=constants.owner_id, text=user.show())
    update.message.reply_text('Я відправив коментар розробнку\n'
                              'ДЯкую за ваше терпіння та заповнення <i>довгої та нудної</i> форми\n',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP,
                              parse_mode='HTML')
    return ConversationHandler.END


def comment_cancel(bot, update):
    chat_id = update.message.chat_id
    USERS_COMMENT.pop(chat_id, None)
    update.message.reply_text('Добре, відміняю',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END


# REGISTRATION
def registration_start(bot, update):
    user = update.message.from_user
    new_user = classes.RegistrationUser(username=user.username, first_name=user.first_name, last_name=user.last_name)
    chat_id = update.message.chat_id
    USERS_REGISTRATION.update({chat_id: new_user})

    markup = ReplyKeyboardMarkup([['/cancel']], resize_keyboard=True)
    update.message.reply_text('Напишіть ваші побажання щодо подарунку що бажаєте отриматм\n'
                              'Подарунок має бути у межах від 0 до 70 грн,\n\nКоитки'
                              '\n\n /cancel для скасування команди',
                              quote=True, parse_mode='HTML', reply_markup=markup)
    return REGISTRATION_END


def registration_end(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text

    user = USERS_REGISTRATION.get(chat_id)
    user.add_wish(text)

    print(user.show())

    update.message.reply_text('Дякую за заповнення форми'
                              'Тепер ви берете участь у грі\n'
                              'Ваша анкета:\n' + user.show(),
                              quote=True, parse_mode='HTML', reply_markup=MAIN_MENU_MARKUP)
    USERS_REGISTRATION.pop(chat_id, None)

    return ConversationHandler.END


def registration_cancel(bot, update):
    chat_id = update.message.chat_id
    USERS_REGISTRATION.pop(chat_id, None)
    update.message.reply_text('Добре, відміняю',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END


comment_handler = ConversationHandler(
        entry_points=[RegexHandler('Залишити коментар', comment)],

        fallbacks=[CommandHandler('cancel', comment_cancel)],
        states={
            MARK: [MessageHandler(Filters.text, comment_mark)],
            CONTACT: [MessageHandler(Filters.text, comment_contact)]
        })

registration_handler = ConversationHandler(
        entry_points=[RegexHandler('Реєстрація', registration_start)],

        fallbacks=[CommandHandler('cancel', registration_cancel)],
        states={
            REGISTRATION_END: [MessageHandler(Filters.text, registration_end)]
        })


# SHOW REGISTERED USERS
def show_users():
    pass


# ADMIN FUNCTIONS


bot_handlers = [CommandHandler('start', start),
                RegexHandler('Вихідний код', source),
                RegexHandler('Подивитись учасників', show_users),
                RegexHandler('Головне меню', main_menu),

                registration_handler,
                comment_handler]
