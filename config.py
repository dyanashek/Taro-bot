import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# manager's id (redirect users to him)
MANAGER_ID = os.getenv('MANAGER_ID')

# bot's ID
BOT_ID = os.getenv('BOT_ID')

# manager's username
MANAGER_USERNAME = os.getenv('MANAGER_USERNAME')

# instagram link
INSTAGRAM_LINK = os.getenv('INSTAGRAM_LINK')

# telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK')

# id of image that displays in text
IMAGE_ID = 'AgACAgIAAxkBAAIIX2RiMdB3_Qtz-yKa2j9RfrMP-HKqAAI_0TEb3cARSwPEL76-G6FVAQADAgADeQADLwQ' # change

# text with terms (start text)
MAIN_TEXT = '''
            \nРада приветствовать\!\
            \nДля получения расшифровки Таро вашей даты рождения ознакомьтесь с правилами: 👇\
            \n\
            \nПравила расшифровки Таро даты рождения:\
            \n1\. дата рождения *1 человека* 🙋‍♂️\
            \n2\. срок *2\-5 дней* ⏱\
            \n3\. быть подписанным на [мою страницу в Instagram](https://instagram.com/yakovleva.anna.taro) 🤳\
            \n4\. дополнительные даты по согласованию 🗓\
            \n\
            \nВаша расшифровка будет готова в течение *2\-5 дней* и я вышлю ее вам _голосовыми сообщениями в Telegram_\.\
            \n\
            \nПолучить расшифровку можно с помощью кнопки, расположенной ниже ⬇️\
            '''

# message that displays if user has already filled the form
FILLED_MESSAGE = 'Вы уже заполняли форму для получения расшифровки.\n\nДля расшифровки дополнительных дат, а так же при возникновении любых вопросов, можно связаться со мной с помощью кнопки, расположенной ниже ⬇️'

# message that displays when user press 'cancel' button
CANCEL_MESSAGE = 'Действие отменено.'

# message that displays when user need to enter his first name
FIRST_NAME_MESSAGE = 'В ответ на это сообщение пришлите Ваше *имя*.'

# message that displays when user need to enter his family name
FAMILY_NAME_MESSAGE = 'В ответ на это сообщение пришлите Вашу *фамилию*.'

# message that displays when user need to enter his instagram link
INSTAGRAM_MESSAGE = 'В ответ на это сообщение пришлите Вашу *ссылку на instagram* _(в формате https://instagram.com/...)_.'

# message that displays when user need to enter his birthday
BIRTHDAY_MESSAGE = 'В ответ на это сообщение пришлите Вашу *вашу дату рождения* _(в формате ДД.ММ.ГГГГ)_.'

# message that displays when user sends wrong information
WRONG_FORMAT_MESSAGE = 'Отправленное Вами сообщение не соответствует требуемому формату или содержит ошибки. Попробуйте еще раз.'

INFO_CATEGORY_IDENTIFIER = {
    'имя' : 'name',
    'фамилию' : 'family',
    'ссылку на instagram' : 'instagram',
    'вашу дату рождения' : 'birth',
}

# message that displays when the form is filled 
FINAL_MESSAGE = '''
            \nВаша расшифровка будет готова в течение 2\-5 дней и я вышлю ее вам голосовыми сообщениями в Telegram\.\
            \nНапоминаю *правила расшифровки* Таро даты рождения:\
            \n\
            \n1\. дата рождения *1 человека* 🙋‍♂️\
            \n2\. срок *2\-5 дней* ⏱\
            \n3\. быть подписанным на [мою страницу в Instagram](https://instagram.com/yakovleva.anna.taro) 🤳\
            \n4\. дополнительные даты по согласованию 🗓\
            \n\
            \nБлагодарю за заявку\!\
            '''