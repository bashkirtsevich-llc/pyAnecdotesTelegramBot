# Telegream anecdotes bot
## Описание
Бот с анекдотами для Telegream, анекдоты хранятся в mongodb.

## Формат данных
CSV формат анекдотов для mongodb: 
```
cat_translit,category,text.
```
В db.journal веедтся журнал использования бота.

![alt text](https://raw.githubusercontent.com/bashkirtsevich/pyAnecdotesTelegramBot/master/bot_view.png "bot interface")

## Необходимые зависимости
```bash
pip install -r bot/requirements.txt
```
