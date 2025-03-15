import telebot
import psycopg2
from conserv import connect_to_server
from datetime import date,datetime
from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel



# load variables from .env file
load_dotenv()

#Take my_id from .env file
my_id = int(os.getenv("MYID"))
# Take bot token from .env file
bot_token = os.getenv("TOKEN")



con, cursor = connect_to_server() 
bot = telebot.TeleBot(bot_token, parse_mode=None)



class Task(BaseModel):
    user_id: int
    message: str
    date_received: None


user_states = {}
def addtoserv(message, data,userid):
    data_to_send = {
        "user_id" : userid,
        "message" : message.text,
        "date_received" : None
    }
    if message.text == 'Отменить':
        del user_states[userid]
        bot.reply_to(message,'Добавление отменено!')
        return None
    try:
        response = requests.post('http://127.0.0.1:8000/add/tasks',json=data_to_send)
        bot.send_message(userid,response.text)
    except Exception as e:
        print('Возникла ошибка: ', e)


def delete_tasks(message,userid):
    data_to_send = {
        "user_id" : userid,
        "message" : message.text,
        "date_received" : None
    }
    response = requests.post('http://127.0.0.1:8000/delete/tasks',json=data_to_send)
    bot.send_message(userid, response.text)
    



def add_completed(message,userid):
    try:
        task_index = int(message) - 1
        now = datetime.now()
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        cursor.execute("SELECT id FROM tasks WHERE users_id = %s", (userid,))
        rows = cursor.fetchall()
        if rows:
            real_task_id = rows[task_index]  
            cursor.execute("SELECT description FROM tasks WHERE id = %s", (real_task_id,))
            task_description = cursor.fetchone()[0]  
            cursor.execute("INSERT INTO completed (users_id,description,date) VALUES (%s,%s,%s)", (userid, task_description,f'{hour}:{minute} {day}.{month}',))
            cursor.execute("DELETE FROM tasks WHERE users_id = %s AND id = %s", (userid, real_task_id))
            bot.send_message(userid, 'Задача успешно завершена. Нажмите на зеленую кнопку чтобы увидеть завершенные задачи!')
        else:
            bot.send_message(userid, 'Нет задач для завершения!')
    except Exception as e:
        print('Возникла ошибка при удалении задачи: ', e)


def getfromserv(mes):
    user_id =  mes.from_user.id
    data_to_send  = {
        "userid": user_id
    }
    response = requests.get('http://127.0.0.1:8000/get/tasks/',params= data_to_send)
    if response.status_code == 404:
        bot.send_message(user_id,'Упс, у вас нет задач')
    else:
        bot.send_message(user_id,response.text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Добавить")
    btn2 = telebot.types.KeyboardButton("Список")
    btn3 = telebot.types.KeyboardButton("Завершить")
    btn4 = telebot.types.KeyboardButton("🗑️")
    btn5 = telebot.types.KeyboardButton("✅")
    markup.add(btn1, btn2,btn3,btn4,btn5)
    try:
        cursor.execute("SELECT * FROM people WHERE user_id = %s", (user_id,))
        result = cursor.fetchall()
        if result:
            bot.reply_to(message, f'Вы уже состоите в нашем боте, попробуйте написать "Добавить", чтобы добавить задачу или "Список", чтобы посмотреть свои задачи!',reply_markup=markup)
        else:
            cursor.execute('INSERT INTO people (user_id) VALUES (%s)', (user_id,))
            bot.send_message(user_id, 'Напишите "Добавить" чтобы создать свою первую задачу, "Список" чтобы посмотреть свой список задач, "Удалить" чтобы удалить задачу из списка', reply_markup=markup)
            con.commit()
    except Exception as e:
        print('Возникла ошибка при добавлении на сервер', e)

@bot.message_handler(commands=['feedback'])
def send_feedback(message):
    user_id = message.from_user.id
    user_states[user_id] = 'waiting for the feedback'
    bot.reply_to(message, 'Напишите, что вы хотите сказать')

@bot.message_handler(commands=['alls'])
def send_feedback(message):
    user_id = message.from_user.id
    if user_id != my_id:
        bot.reply_to(message, 'Вы не можете использовать эту команду')
    response = requests.get('http://127.0.0.1:8000/get/feedbacks')
    bot.send_message(my_id,response.text)
  

@bot.message_handler()
def showdata(message):
    user_id =  message.from_user.id
    denb = date.today()
    now = datetime.now()
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    msg = message.text
    cursor.execute("SELECT * FROM people WHERE user_id = %s", (user_id,))
    user = cursor.fetchall()
    if not user:
        bot.reply_to(message, 'Упс, не вижу вас в базе, напишите "/start" чтобы приступить к работе!')
        return
    if msg.lower() == 'список':
        getfromserv(message)
    
    if msg.lower() == '✅':
        try:
            cursor.execute("SELECT description FROM completed WHERE users_id = %s", (str(user_id),))
            completes = cursor.fetchall()
            if completes:
                result = '\n'.join([f'{index + 1}.{str(row[0])}' for index,row in enumerate(completes)]) 
                bot.send_message(user_id, f'Ваш список завершенных дел! Радуйтесь собой✅ \n{result}')
                bot.send_message(user_id, 'Поздравляем, вы большой молодец!')
        except Exception as e:
            bot.reply_to(message, f'Возникла ошибка! Пожалуйста повторите ваш запрос!{e}')
        
    

    if msg.strip().lower() == 'завершить':  
        bot.reply_to(message, 'Выберите задачу из списка которую вы хотите завершить!')
        user_states[user_id] = 'waiting for to be completed'
    elif user_id in user_states and user_states[user_id] == 'waiting for to be completed': 
            add_completed(msg,user_id)
            del user_states[user_id] 

    if msg.strip().lower() == 'добавить':  
        bot.reply_to(message, 'Сформулируйте вашу задачу и отправьте ее боту!')
        user_states[user_id] = 'waiting for the answer' 
    elif user_id in user_states and user_states[user_id] == 'waiting for the answer': 
            addtoserv(message, denb, user_id)
            del user_states[user_id] 

    if msg.lower() == '🗑️':
        bot.reply_to(message, 'Укажите номер задачи из списка которую вы хотите удалить')
        user_states[user_id] = 'waiting for the id to delete' 
    
    elif user_id in user_states and user_states[user_id] == 'waiting for the id to delete':
        delete_tasks(msg,user_id)
        del user_states[user_id] 

    elif user_id in user_states and user_states[user_id] == 'waiting for the feedback':
        try:
            cursor.execute("INSERT INTO feedbacks2 (text, date) VALUES (%s,%s)", (message.text,f'{hour}:{minute} {day}.{month}',))
            bot.reply_to(message, 'Ваш отзыв сохранен!')
            bot.send_message(my_id, 'Макс, тебе пришел новый отзыв /alls')
        except Exception as e:
            print('Возникла ошибка при добавлении отзыва', e)
        del user_states[user_id] 
    
        
    con.commit()

try:
    now = datetime.now()
    second = now.second
    bot.infinity_polling()
finally:
    con.close()
