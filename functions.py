import sqlite3
import logging
import inspect
import gspread
import datetime
import telebot

import keyboards
import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

service_acc = gspread.service_account(filename='service_account.json')
sheet = service_acc.open(config.SPREAD_NAME)
work_sheet = sheet.worksheet(config.LIST_NAME)

def is_new_user(user_id):
    """Checks if user already in database. 
    Returns an empty list if the user is new.
    """

    database = sqlite3.connect("taro.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    user = cursor.execute(f"SELECT * FROM users WHERE user_id='{user_id}'").fetchall()

    cursor.close()
    database.close()

    if user != []:
        user = user[0]
    
    return user


def add_user(user_id, user_username):
    """Adds a new user to database."""

    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''
            INSERT INTO users (user_id, user_username)
            VALUES ("{user_id}", "{user_username}")
            ''')

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Добавлен новый пользователь {user_username}.')


def is_form_filled(info):
    """Checks if user has already filled the form. 
    Return False if he doesn't"""

    if None in info:
        return False
    
    return True


def set_to_none(user_id):
    """Sets all filled fields to None."""

    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET name=NULL, family=NULL, instagram=NULL, birth=NULL
                    WHERE user_id="{user_id}"
                    ''')

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Сброшены заполненные поля пользователя {user_id}.')


def name_response(first_name):
    """Generates a response, depends on first name."""

    if first_name is None:
        keyboard = keyboards.enter_name_keyboard()
        reply_text = config.FIRST_NAME_MESSAGE
    else:
        keyboard = keyboards.confirm_first_name_keyboard(first_name)
        reply_text = f'Ваше имя - *{first_name}*?'

    return reply_text, keyboard


def family_name_response(family_name):
    """Generates a response, depends on family name."""

    if family_name is None:
        keyboard = keyboards.enter_family_name_keyboard()
        reply_text = config.FAMILY_NAME_MESSAGE
    else:
        keyboard = keyboards.confirm_family_name_keyboard(family_name)
        reply_text = f'Ваша фамилия - *{family_name}*?'

    return reply_text, keyboard


def enter_response(info_category):
    """Generates a response when user wants to enter something manual."""

    if info_category == 'name':
        keyboard = keyboards.enter_name_keyboard()
        reply_text = config.FIRST_NAME_MESSAGE
    
    elif info_category == 'family':
        keyboard = keyboards.enter_family_name_keyboard()
        reply_text = config.FAMILY_NAME_MESSAGE

    return reply_text, keyboard


def fill_form_info(info_category, info, user_id):
    """Fill one of the form field."""

    database = sqlite3.connect("taro.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET {info_category}="{info}"
                    WHERE user_id="{user_id}"
                    ''')

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: У пользователя {user_id} заполнена графа {info_category} ({info}).')


def confirm_form_reply(name, family_name, instagram_link, birthday):
    """Constructs a text to confirm filled info."""

    reply_text = f'''
                \nВы ввели следующие данные:\
                \n\
                \n*Имя*: {name}\
                \n*Фамилия:* {family_name}\
                \n*Instagram:* {instagram_link}\
                \n*Дата рождения:* {birthday}\
                '''
    
    return reply_text


def transfer_to_google_sheets(user_id):
    """Transfers data to google sheets."""

    user_info = list(is_new_user(user_id))
    user_info = user_info[1::]

    birthday = datetime.datetime.strftime(user_info[-1], "%d.%m.%Y")
    user_info[-1] = birthday

    fill_date = datetime.datetime.strftime((datetime.datetime.utcnow() + datetime.timedelta(hours=3)).date(), "%d.%m.%Y")
    user_info.append(fill_date)

    row = get_row()

    try:
        work_sheet.update(f'A{row}:G{row}', [user_info])
    except:
        pass

    logging.info(f'{inspect.currentframe().f_code.co_name}: Данные пользователя {user_id} внесены в таблицу.')


def get_row():
    """Gets the number of first empty row in table."""

    return len(work_sheet.col_values(1)) + 1


def notify_manager(user_id):
    """Notifies manager that user filled up the form."""

    user_info = is_new_user(user_id)

    username = user_info[2]
    name = user_info[3]
    family_name = user_info[4]
    instagram_link = user_info[5]
    birthday = datetime.datetime.strftime(user_info[6], "%d.%m.%Y")

    reply_text = f'''
                \nПользователь @{username} отправил форму на расшифровку:\
                \n\
                \n*Имя:* {name}\
                \n*Фамилия:* {family_name}\
                \n*Instagram:* {instagram_link}\
                \n*День рождения:* {birthday}\
                '''
    try:
        message = bot.send_message(chat_id=config.MANAGER_ID,
                         text=reply_text,
                         reply_markup=keyboards.mark_as_complete(user_id),
                         parse_mode='Markdown',
                         )
        bot.pin_chat_message(chat_id=config.MANAGER_ID,
                             message_id=message.id,
                             disable_notification=True,
                             )
    except:
        pass


def color_spread(user_id):
    """Colors the row to green after answering the request."""

    row = get_color_row(user_id)

    work_sheet.format(f'A{row}:G{row}', {"backgroundColor": {"red": 0.4, "green": 0.67, "blue": 0.51}})


def get_color_row(user_id):
    """Gets the number of row that should be colored."""

    return work_sheet.col_values(1).index(user_id) + 1

