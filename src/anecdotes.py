#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import random
import re
import time


class Anecdotes(object):
    def __init__(self):
        self.__client = MongoClient('mongodb://localhost:27017/')
        self.__db = self.__client.anecdotes

        self.__categories = self.__db.anecdotes.distinct("cat_translit")

    @property
    def categories(self):
        return self.__categories

    def write_fail_log(self, message):
        log_item = {
            "time": int(time.time()),
            "message": message
        }
        self.__db.fails.insert_one(log_item)

    def write_messages_log(self, message):
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
        self.__db.journal.insert_one(log_item)

    def __fetch_anecdote(self, cursor):
        def normalize_text(text):
            _ = text
            _ = "\r\n".join(_.split("\\n"))
            _ = "\"".join(_.split("&quot;"))
            return _

        if cursor.count() > 0:
            anecdote = cursor[random.randrange(cursor.count())]
            return u"Из категории: " + anecdote["category"] + " (/" + anecdote[
                "cat_translit"] + ")\r\n" + normalize_text(anecdote["text"])
        else:
            return u"Не найдено ничего интересного"

    def get_anecdote_by_match(self, match):
        return self.__fetch_anecdote(
            self.__db.anecdotes.find(
                {"text":
                    re.compile(
                        "|".join(
                            filter(lambda it: len(it) > 0, match.split(" "))
                        ), re.IGNORECASE
                    )
                }
            )
        )

    def get_anecdote_by_category(self, category):
        return self.__fetch_anecdote(self.__db.anecdotes.find({"cat_translit": category}))

    def get_statistics(self):
        users = self.__db.journal.distinct("user")
        queries = reduce(lambda r, t: r + "\r\n" + t, self.__db.journal.distinct("text"))
        return users, queries
