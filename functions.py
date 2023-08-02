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
    user_info = user_info[1:7:]
    print(user_info)

    birthday = datetime.datetime.strftime(user_info[5], "%d.%m.%Y")
    user_info[5] = birthday

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


def update_service(user_id, service):
    """Sets all filled fields to None."""

    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET service=?
                    WHERE user_id=?
                    ''', (service, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_username(user_id, username):
    """Sets all filled fields to None."""

    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET user_username=?
                    WHERE user_id=?
                    ''', (username, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_request(user_id, request, request_type):
    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET request=?, request_type=?
                    WHERE user_id=?
                    ''', (request, request_type, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_check(user_id, check, check_type):
    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET check_id=?, check_type=?
                    WHERE user_id=?
                    ''', (check, check_type, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_photo(user_id, photo):
    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET photo=?
                    WHERE user_id=?
                    ''', (photo, user_id,))

    database.commit()
    cursor.close()
    database.close()


def drop_payment(user_id):
    """Sets all filled fields to None."""

    database = sqlite3.connect("taro.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET service=NULL, check_id=NULL, check_type=NULL, photo=NULL, request=NULL, request_type=NULL
                    WHERE user_id="{user_id}"
                    ''')

    database.commit()
    cursor.close()
    database.close()


def handle_payment(user_id):
    user_info = is_new_user(user_id)

    username = user_info[2]
    service = user_info[7]
    check_id = user_info[8]
    check_type = user_info[9]
    photo = user_info[10]
    request = user_info[11]
    request_type = user_info[12]

    drop_payment(user_id)
    transfer_to_google_sheets_payments(user_id, username, config.SERVICES_NAMES[service])

    try:
        bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Пользователь @{username} оплатил услугу: *{config.SERVICES_NAMES[service]}*.',
                         parse_mode='Markdown',
                         )
        
        check_message = bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Платежный документ пользователя @{username}:',
                         )
        
        if check_type == 'document':
            bot.send_document(chat_id=config.MANAGER_ID,
                              document=check_id,
                              reply_to_message_id=check_message.id,
                              )
        else:
            bot.send_photo(chat_id=config.MANAGER_ID,
                            photo=check_id,
                            reply_to_message_id=check_message.id,
                            )
            
        bot.send_photo(chat_id=config.MANAGER_ID,
                            photo=photo,
                            caption=f'Селфи пользователя @{username}.',
                            )
        
        request_message = bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Запрос пользователя @{username}:',
                         )
        
        if request_type == 'text':
            bot.send_message(chat_id=config.MANAGER_ID,
                              text=request,
                              reply_to_message_id=request_message.id,
                              )
        else:
            try:
                bot.send_audio(chat_id=config.MANAGER_ID,
                                audio=request,
                                reply_to_message_id=request_message.id,
                                )
            except Exception as ex:
                print(ex)
    except:
        pass


def get_payment_row():
    """Gets the number of first empty row in table."""

    work_sheet_payments = sheet.worksheet(config.PAYMENT_LIST)
    return len(work_sheet_payments.col_values(1)) + 1


def transfer_to_google_sheets_payments(user_id, username, service):
    """Transfers data to google sheets."""

    row = get_payment_row()

    work_sheet_payments = sheet.worksheet(config.PAYMENT_LIST)

    fill_date = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(hours=3), "%d.%m.%Y %H:%M")

    try:
        work_sheet_payments.update(f'A{row}:D{row}', [[user_id, username, service, fill_date]])
    except:
        pass