"""
Chatbot starter
"""
import telebot
import json

with open('clear_data.json', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

bot = telebot.TeleBot("7754776786:AAFXPPZpJr7_GmUY_fB6aH-4sro05JKXmYE", parse_mode=None)

#1 BLOCK
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, '''Привет, меня зовут КЛУБень!
Я бот студентов ФиПЛа, который поможет тебе разобраться во внеучебной деятельности Нижнегородской Вышки.

Здесь ты можешь найти информацию по действующим клубам, контактные данные для создания собственного клуба и многое другое. 

Давай расскажу!''')
    ask_about_add_activities(message)
#2 BLOCK
def ask_about_add_activities(message):
    text = "<Интересна ли пользователю внеучебная деятельность, а именно клубы ВШЭ>"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown") #if we need to highlight some info
    bot.register_next_step_handler(sent_msg, process_add_activities)

def process_add_activities(message):
    if message.text == 'Да': # not only
        ask_about_interests(message)
    else:
        bot.send_message(message.chat.id, "<Прощание, ничем не можем помочь)> \n Если передумаешь и захочешь начать снова, нажми на /start")
#3 BLOCK
def ask_about_interests(message):
    text = "<Ввод интересов, хобби для подбора клубов>"
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, choose_subject)

#4 BLOCK
def choose_subject(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Творческое начало', callback_data='1'))
    markup.add(telebot.types.InlineKeyboardButton('Бизнес и эрудиция', callback_data='2'))
    markup.add(telebot.types.InlineKeyboardButton('Организация мероприятий', callback_data='3'))
    markup.add(telebot.types.InlineKeyboardButton('СМИ и медиа', callback_data='4'))
    markup.add(telebot.types.InlineKeyboardButton('Большая социальная миссия', callback_data='5'))
    markup.add(telebot.types.InlineKeyboardButton('Спорт и увлечения', callback_data='6'))
    markup.add(telebot.types.InlineKeyboardButton('Студенческий совет', callback_data='7'))
    markup.add(telebot.types.InlineKeyboardButton('Волонтёрский центр', callback_data='8'))
    markup.add(telebot.types.InlineKeyboardButton('Ничего не заинтересовало', callback_data='9'))

    bot.send_message(message.chat.id, "<Подбор подходящих тематик клубов>", reply_markup=markup)

#5-6 BLOCK
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call, message):
    if call.data == '1':
        subject = data['Творческое начало']
        info_1 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_1} \n")
        choose_club(call.message, subject)
    elif call.data == '2':
        subject = data['Бизнес и эрудиция']
        info_2 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_2} \n")
        choose_club(call.message, subject)
    elif call.data == '3':
        subject = data['Организация мероприятий']
        info_3 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_3} \n")
        choose_club(call.message, subject)
    elif call.data == '4':
        subject = data['СМИ и медиа']
        info_4 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_4} \n")
        choose_club(call.message, subject)
    elif call.data == '5':
        subject = data['Большая социальная миссия']
        info_5 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_5} \n")
        choose_club(call.message, subject)
    elif call.data == '6':
        subject = data['Спорт и увлечения']
        info_6 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_6} \n")
        choose_club(call.message, subject)
    elif call.data == '7':
        subject = data['Студенческий совет']
        info_7 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_7} \n")
        choose_club(call.message, subject)
    elif call.data == '8':
        subject = data['Волонтёрский центр']
        info_8 = '\n'.join(list( f"{i} \n {subject[i][1]}" for i in subject.keys()))
        bot.send_message(call.message.chat.id, f"Отличный выбор! \n <Выбор конкретного клуба по тематике> \n {info_8} \n")
        choose_club(call.message, subject)
    elif call.data == '9':
        bot.send_message(call.message.chat.id, "<Прощание, ничем не можем помочь)> \n Если передумаешь и захочешь начать снова, нажми на /start")

    text = "<Хотели бы узнать дополнительную информацию?>"
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, choose_club)
#7 BLOCK

def choose_club(message, subject):
    clubs = list(i for i in subject.keys())
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(clubs[0], callback_data='1'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[1], callback_data='2'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[2], callback_data='3'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[3], callback_data='4'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[4], callback_data='5'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[5], callback_data='6'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[6], callback_data='7'))
    markup.add(telebot.types.InlineKeyboardButton(clubs[7], callback_data='8'))
    markup.add(telebot.types.InlineKeyboardButton('Ничего не заинтересовало', callback_data='9'))

    bot.send_message(message.chat.id, "<Подбор клубов>", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(message, call, subject, clubs):
    if call.data == '1':
        link = subject[clubs[0]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '2':
        link = subject[clubs[1]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '3':
        link = subject[clubs[2]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '4':
        link = subject[clubs[3]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '5':
        link = subject[clubs[4]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '6':
        link = subject[clubs[5]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '7':
        link = subject[clubs[6]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '8':
        link = subject[clubs[7]][0]
        info = '<Доп инфа>'
        bot.send_message(call.message.chat.id, f"{subject} '\n' {link} '\n' {info}")
    elif call.data == '9':
        bot.send_message(call.message.chat.id, "<Прощание, ничем не можем помочь)> \n Если передумаешь и захочешь начать снова, нажми на /start")
    bot.send_message(message.chat.id, "that's all")

bot.polling()
# bot.infinity_polling()