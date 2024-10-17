"""
Chatbot starter
"""
# pylint: disable=invalid-name,too-many-branches
import json

import telebot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

with open('dataset/clear_data.json', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

with open ('dataset/questions.json', encoding='utf-8', errors='ignore') as q:
    questions = json.load(q)
    additional_questions = '\n\n'.join(list((f'<b>{k}</b>\n    — {v}'
                                             for k, v in questions.items())))

# save the token
bot = telebot.TeleBot("7604474051:AAErnNbDz427QWCrT4IBl039aCebdZx17fM", parse_mode=None)
subjects = list(i for i in data.keys())
not_bye = 'Надеюсь, что смог помочь тебе и информация была полезной! \n' \
          'А если тебя ничего не заинтересовало, может, ты хочешь создать свой ' \
          'собственный клуб? В таком случае можно обратиться к **Шмелёву Степану' \
          ' Викторовичу** - главе внеучебной деятельности НИУ ВШЭ \n' \
          'https://vk.com/id307399746 \n\nДо новых встреч :)' \
          '\n\n Если захочешь снова начать со мной общение, нажми на /start'


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call: CallbackQuery) -> None:
    """
    Button handler

    Args:
        call (CallbackQuery): call
    """
    if call.data == "yes":
        ask_about_subject(call.message)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Мне жаль, что тебе не интересна"
                                               " внеучебная деятельность. \n\nНо если"
                                               " ты всё же передумаешь и захочешь "
                                               "начать снова, нажми на /start \n\n"
                                               "Надеюсь, что буду полезным в будущем :)")
    elif call.data in ['0', '1', '2', '3', '4', '5']:
        subject_index = int(call.data)
        markup, message = get_clubs(subject_index)
        bot.send_message(call.message.chat.id, message, reply_markup=markup)
    elif call.data in data[subjects[0]].keys():
        club_info = get_club_info(call.data, 0)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data in data[subjects[1]].keys():
        club_info = get_club_info(call.data, 1)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data in data[subjects[2]].keys():
        club_info = get_club_info(call.data, 2)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data in data[subjects[3]].keys():
        club_info = get_club_info(call.data, 3)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data in data[subjects[4]].keys():
        club_info = get_club_info(call.data, 4)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data in data[subjects[5]].keys():
        club_info = get_club_info(call.data, 5)
        bot.send_message(call.message.chat.id, club_info)
    elif call.data == '6':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Студенческий совет', callback_data='stud_consule'))
        bot.send_message(call.message.chat.id, "Студенческий совет - отличный выбор! \n"
                                               "Ты можешь узнать подробную информацию о клубе,"
                                               " нажав на одну из кнопок ниже \n",
                         reply_markup=markup)
    elif call.data == '7':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Волонтёрский центр', callback_data='volunteer_center'))
        bot.send_message(call.message.chat.id, "Волонтёрский центр- отличный выбор! \n"
                                               "Ты можешь узнать подробную информацию о клубе,"
                                               " нажав на одну из кнопок ниже \n",
                         reply_markup=markup)
    elif call.data == 'None':
        bot.send_message(call.message.chat.id, not_bye,  parse_mode='Markdown')
    elif call.data == 'stud_consule':
        club_info = data['Студенческий совет']
        bot.send_message(call.message.chat.id, f'Студенческий совет '
                                               f'\n\n{club_info[1]}\n \n \n'
                                               f' Подробнее о клубе можешь узнать '
                                               f'здесь: \n{club_info[0]}')
    elif call.data == 'Волонтёрский центр':
        club_info = data['volunteer_center']
        bot.send_message(call.message.chat.id, f'Волонтёрский центр '
                                               f'\n\n{club_info[1]}\n \n \n'
                                               f' Подробнее о клубе можешь узнать'
                                               f' здесь: \n{club_info[0]}')
    elif call.data == "additional_info":
        bot.send_message(call.message.chat.id, additional_questions, parse_mode='HTML')


# 1 BLOCK
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message) -> None:
    """
    Welcome message

    Args:
        message (Message): message
    """
    bot.reply_to(message, '''Привет, меня зовут КЛУБень!
Я бот студентов ФиПЛа, который поможет тебе разобраться во внеучебной деятельности Нижнегородской Вышки.

Здесь ты можешь найти информацию по действующим клубам, контактные данные для создания собственного клуба и многое другое.

Давай расскажу!''')
    ask_about_add_activities(message)


# 2 BLOCK
def ask_about_add_activities(message: Message) -> None:
    """
    First question

    Args:
         message (Message): message
    """
    text = "Хотел бы ты больше узнать о внеучебных клубах Нижегородской вышки?"
    markup = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton("Да!", callback_data="yes")
    no_button = InlineKeyboardButton("Нет(", callback_data="no")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, text, reply_markup=markup)


# 3 BLOCK
def ask_about_subject(message: Message) -> None:
    """
    Theme question

    Args:
        message (Message): message
    """
    text = "В Нижегородской вышке есть следующие направления внеучебной деятельности:"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Творческое начало', callback_data='0'))
    markup.add(InlineKeyboardButton('Бизнес и эрудиция', callback_data='1'))
    markup.add(InlineKeyboardButton('Организация мероприятий', callback_data='2'))
    markup.add(InlineKeyboardButton('СМИ и медиа', callback_data='3'))
    markup.add(InlineKeyboardButton('Большая социальная миссия', callback_data='4'))
    markup.add(InlineKeyboardButton('Спорт и увлечения', callback_data='5'))
    markup.add(InlineKeyboardButton('Студенческий совет', callback_data='6'))
    markup.add(InlineKeyboardButton('Волонтёрский центр', callback_data='7'))

    bot.send_message(message.chat.id, text, reply_markup=markup)
    sent_msg = "Ну как? Есть что-то интересное именно для тебя?" \
               " Нажми на кнопку выше и выбери направление, чтобы " \
               "узнать, какие клубы туда входят"
    bot.send_message(message.chat.id, sent_msg)

    additional_message = "Если тебя ничего не заинтересовало," \
                         " или ты хочешь узнать дополнительную" \
                         " информацию, нажми на кнопку ниже"
    additional_markup = InlineKeyboardMarkup()
    additional_info_button = InlineKeyboardButton("Дополнительная информация",
                                                  callback_data="additional_info")
    nothing_interested_button = InlineKeyboardButton("Ничего не заинтересовало",
                                                     callback_data='None')

    additional_markup.add(additional_info_button, nothing_interested_button)
    bot.send_message(message.chat.id, additional_message, reply_markup=additional_markup)


# 4 BLOCK
def get_clubs(subject_index: int) -> tuple[InlineKeyboardMarkup, str]:
    """
    Club getting from theme index

    Args:
         subject_index (int): theme index
    """
    subject = data[subjects[subject_index]]
    clubs = list(i for i in subject.keys())

    markup = InlineKeyboardMarkup()
    buttons = []
    for club in clubs[:10]:
        button = InlineKeyboardButton(club, callback_data=club)
        buttons.append(button)
    markup.add(*buttons)
    return markup, f"{subjects[subject_index]} - отличный выбор! \n" \
                   f"Ты можешь узнать подробную информацию о клубе," \
                   f"нажав на одну из кнопок ниже \n"


# 5 BLOCK
def get_club_info(club_name: str, subject_index: int) -> str:
    """
    Club info getting

    Args:
        club_name (str): club name
        subject_index (int): club theme index
    """
    subject = data[subjects[subject_index]]
    club_info = subject[club_name]
    return f"{club_name} \n\n{club_info[1]}\n \n \n" \
           f"Подробнее о клубе можешь " \
           f"узнать здесь: \n{club_info[0]}"


@bot.message_handler(content_types=['text'])
def handle_text(message: Message) -> None:
    """
    Text handling

    Args:
        message (Message): text
    """
    text_markup = 'Извини, не могу ответить на твое сообщение\nВозможно,' \
                  ' ты найдешь интересующую информацию ниже по кнопке?'
    add_text_markup = InlineKeyboardMarkup()
    text_message = InlineKeyboardButton("Дополнительная информация",
                                        callback_data="additional_info")
    add_text_markup.add(text_message)
    bot.send_message(message.chat.id, text_markup, reply_markup=add_text_markup)


bot.polling()  # for a while
