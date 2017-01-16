# Telegream anecdotes bot
## Описание
Бот с анекдотами для Telegream, анекдоты хранятся в mongodb.

## Формат данных
CSV формат анекдотов для mongodb: 
```
cat_translit,category,text.
```
В db.journal веедтся журнал использования бота.

![alt text](https://raw.githubusercontent.com/bashkirtsevich/pyAnecdotesTelegramBot/master/bot_view.png "bot example")

## Необходимые компоненты
pytelegrambotapi:
```bash
python -m pip install pytelegrambotapi
```
pymongo:
```bash
python -m pip install pymongo
```
