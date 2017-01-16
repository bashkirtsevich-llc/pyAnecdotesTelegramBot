#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import telebot
from pymongo import MongoClient
import random
import re
import time


def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.anecdotes

    categories = db.anecdotes.distinct("cat_translit")

    def extract_command(text):
        def is_command(text):
            return text.startswith('/')

        return text.split()[0].split('@')[0][1:] if is_command(text) else None

    def normalize_text(text):
        result = text
        result = "\r\n".join(result.split("\\n"))
        result = "\"".join(result.split("&quot;"))
        return result

    def write_fail_log(message):
        log_item = {
            "time": int(time.time()),
            "message": message
        }
        db.fails.insert_one(log_item)

    def write_messages_log(message):
        log_item = {
            "user": {
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "id": message.from_user.id
            },
            "text": message.text,
            "date": message.date
        }
        db.journal.insert_one(log_item)

    def fetch_anecdote(cursor):
        if cursor.count() > 0:
            anecdote = cursor[random.randrange(cursor.count())]
            return u"Из категории: " + anecdote["category"] + " (/" + anecdote[
                "cat_translit"] + ")\r\n" + normalize_text(anecdote["text"])
        else:
            return config.not_found_string

    def get_anecdote_by_match(match):
        return fetch_anecdote(db.anecdotes.find({"text": re.compile("|".join(
            filter(lambda it: len(it) > 0, match.split(" "))
        ), re.IGNORECASE)}))

    def get_anecdote_by_category(category):
        return fetch_anecdote(db.anecdotes.find({"cat_translit": category}))

    def get_bot_stat():
        users = db.journal.distinct("user")
        queries = reduce(lambda r, t: r + "\r\n" + t, db.journal.distinct("text"))
        return users, queries

    bot = telebot.TeleBot(config.token)

    @bot.message_handler(commands=["start", "help"])
    def handle_start_help(message):
        bot.send_message(message.chat.id, config.help_string)

    @bot.message_handler(commands=["stat"])
    def handle_stat(message):
        users, queries = get_bot_stat()
        stat = u"Пользователей:\r\n" + str(len(users)) + "\r\n" +  \
               u"Запросы:\r\n" + queries

        bot.send_message(message.chat.id, stat)

    @bot.message_handler(commands=categories)
    def handle_category(message):
        write_messages_log(message)
        bot.send_message(message.chat.id, get_anecdote_by_category(extract_command(message.text)))

    @bot.message_handler(content_types=["text"])
    def send_anecdote(message):
        write_messages_log(message)
        bot.send_message(message.chat.id, get_anecdote_by_match(message.text))

    # start polling
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt, SystemExit:
        raise
    except Exception, e:
        write_fail_log(str(e))
        raise


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt, SystemExit:
            break
        except:
            time.sleep(10)
            pass
