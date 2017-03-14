#!/usr/bin/env python
# -*- coding: utf-8 -*-

from anecdotes import Anecdotes
import config
import telebot


def main():
    base = Anecdotes()

    while True:
        try:
            bot = telebot.TeleBot(config.token, threaded=False)

            @bot.message_handler(commands=["start", "help"])
            def handle_start_help(message):
                help_string = "Привет, я бот с кучей анекдотов, отправь мне сообщение с тематикой анекдота " \
                              "и я постараюсь найти тебе что-нибудь, чтоб ты смеялся, сука, до усрачки бля!"
                bot.send_message(message.chat.id, help_string)

            @bot.message_handler(commands=["stat"])
            def handle_stat(message):
                users, queries = base.get_statistics()
                stat = u"Пользователей:\r\n" + str(len(users)) + "\r\n" + \
                       u"Запросы:\r\n" + queries

                bot.send_message(message.chat.id, stat)

            @bot.message_handler(commands=base.categories)
            def handle_category(message):

                def extract_command(text):
                    return text.split()[0].split('@')[0][1:] if text.startswith('/') else None

                base.write_messages_log(message)
                bot.send_message(message.chat.id, base.get_anecdote_by_category(extract_command(message.text)))

            @bot.message_handler(content_types=["text"])
            def send_anecdote(message):
                base.write_messages_log(message)
                bot.send_message(message.chat.id, base.get_anecdote_by_match(message.text))

            # start polling
            bot.polling(none_stop=True)
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            base.write_fail_log(str(e))


if __name__ == '__main__':
    main()
