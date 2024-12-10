import psycopg2
import telebot
from telebot import types

connection = psycopg2.connect(
    host="localhost",
    database="adminpanelbot",
    user="postgres",
    password="MH2012"
)
cursor = connection.cursor()

create_table1 = '''
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        telegram_id VARCHAR(100) NOT NULL,
        username VARCHAR(100) NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''
cursor.execute(create_table1)
connection.commit()

tasks = '''
    CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        telegram_id VARCHAR(100) NOT NULL,
        tasks VARCHAR(100) NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''
cursor.execute(tasks)
connection.commit()

BOT_TOKEN = "7879865972:AAH7kb293WAIXwOvb3oorm3Urw-lGTNX1I0"
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}
def admin(telegram_id):
    select = '''
        SELECT * FROM users WHERE telegram_id = %s;
    '''
    cursor.execute(select, (telegram_id,))
    connection.commit()
    users = cursor.fetchone()
    if users:
        return True

def user(telegram_id):
    select = '''
            SELECT * FROM users WHERE telegram_id = %s;
        '''
    cursor.execute(select, (telegram_id,))
    connection.commit()
    users = cursor.fetchone()
    if users:
        return True

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Es Adminnem", callback_data="es_adminnem")
    btn2 = types.InlineKeyboardButton("Es Usernnem", callback_data="es usernnem")
    markup.add(btn1, btn2)
    bot.reply_to(message, "yntreq kocakneric voreve meky", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    if call.data == "es_adminnem":
        if admin(str(user_id)):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Tesnel Bolor Asxatakicnerin", callback_data="tesnel")
            btn2 = types.InlineKeyboardButton("Avelacnel Asxatakic", callback_data="avelacnel")
            btn3 = types.InlineKeyboardButton("Uxarkel Arajadranq", callback_data="uxarkel")
            markup.add(btn1, btn2, btn3)
            bot.send_message(call.message.chat.id, "Bari galust dzer asxatanqayin panel", reply_markup=markup)
    elif call.data == "es usernnem":
        if user(str(user_id)):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Tesnel Im arajadranqery", callback_data="tesnel_arajadranq")
            markup.add(btn1)
            bot.send_message(call.message.chat.id, "Bari galust dzer arajadranqeri panel", reply_markup=markup)
    elif call.data == "tesnel":
        select = '''
                    SELECT * FROM users;
                '''
        cursor.execute(select)
        connection.commit()
        users = cursor.fetchall()
        bot.send_message(call.message.chat.id, f"{users}")
    elif call.data == "avelacnel":
        bot.send_message(call.message.chat.id, "Greq ayd mardu telegram aydin")
        @bot.message_handler(content_types=["text"])
        def avelacnel(message):
            if "telegram_id" not in user_data:
                telegram_id = message.text
                user_data["telegram_id"] = telegram_id
                bot.reply_to(message, "Hima Greq ayd mardu anuny")
            else:
                user_name = message.text
                user_data["user_name"] = user_name
                insert = '''
                    INSERT INTO users (telegram_id, username) VALUES (%s, %s);
                '''
                cursor.execute(insert, (str(user_data["telegram_id"]), user_data["user_name"],))
                connection.commit()
                insert2 = '''
                    INSERT INTO tasks (telegram_id, tasks) VALUES(%s, %s);
                '''
                cursor.execute(insert2, (str(user_data["telegram_id"]), "Duq Aysor der arajadranq chuneq"))
                connection.commit()
    elif call.data == "uxarkel":
        bot.send_message(call.message.chat.id, "Greq arajadranqy")
        @bot.message_handler(content_types=["text"])
        def arajadranq(message):
            if "tasks" not in user_data:
                tasks = message.text
                user_data["tasks"] = tasks
                bot.reply_to(message, "Hima greq ayd mardu telegram id")
            else:
                telegram_id = message.text
                user_data["telegram_id2"] = telegram_id
                update = '''
                    UPDATE tasks SET tasks = %s WHERE telegram_id = %s; 
                '''
                cursor.execute(update, (user_data["tasks"], str(user_data["telegram_id2"]),))
                connection.commit()
    elif call.data == "tesnel_arajadranq":
        select = '''
            SELECT * FROM tasks WHERE telegram_id = %s;
        '''
        cursor.execute(select, (str(user_id),))
        connection.commit()
        users = cursor.fetchone()
        bot.send_message(call.message.chat.id, f"{users[2]}")
bot.polling()