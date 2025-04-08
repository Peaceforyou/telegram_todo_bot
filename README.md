# telegram_todo_bot
Telegram bot created with telebot library and postresql

It allows you to run it on your telegram bot id.

In order to that you should create .env file and fill it like in .env.example

Next, install all requirements with pip install -r requirements.txt

After that you should run app by commands:

python main.py     #    telegram bot
uvicorn thrapi:app --reload   #    api to connect database with bot

And you will be able to manage your task right in your telegram chat
