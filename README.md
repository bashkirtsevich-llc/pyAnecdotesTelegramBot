# Telegream anecdotes bot
Бот с анекдотами для Telegream, анекдоты хранятся в mongodb.

CSV формат анекдотов для mongodb: cat_translit,category,text.
В db.journal веедтся журнал использования бота.

![alt text](https://raw.githubusercontent.com/bashkirtsevich/pyAnecdotesTelegramBot/master/bot_view.png "bot example")

## Необходимые компоненты
pytelegrambotapi:
```bash
pip install pytelegrambotapi
```
pymongo:
```bash
pip install pymongo
```
