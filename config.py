import os
from dotenv import load_dotenv

import text

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
IMAGE_ID = 'AgACAgIAAxkBAAMLZMJs1VaWNIrKhZkfivRfKjs6ktMAAj_RMRvdwBFLhq5Xqe4mJ8cBAAMCAAN5AAMvBA' # change AgACAgIAAxkBAAMzZGMy1NAueN5fcK1VQvFrgbhpnGwAAj_HMRt9NCFLyKsPuzheBgsBAAMCAAN5AAMvBA

MENU_IMAGE = 'AgACAgIAAxkBAAIcOWTHVxscDXawd45CWDR32F5SdtPHAAJd0DEb9945SrUSUJjP9NTsAQADAgADeQADLwQ'

SPREAD_NAME = 'Код Таро даты рождения'
LIST_NAME = 'Заявки'
PAYMENT_LIST = 'Платежи'

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
            \n\
            \nОтблагодарить меня за инсайты можно переводом любой суммы на карты:\
            \nДля граждан России:\
            \n5469380092114452\
            \n\
            \nДля граждан других государств:\
            \n5269880013129754\
            \nIBAN $:\
            \nKZ30551B229777462USD\
            \n\
            \nIBAN€\
            \nKZ77551B229750110EUR\
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

CHECK_MESSAGE = 'В ответ на это сообщение пришлите чек об оплате услуги (скриншот или файл).'

PHOTO_MESSAGE = 'В ответ на это сообщение пришлите Ваше селфи (на фото должны быть только Вы без посторонних людей и животных, как можно самое свежее).'

REQUEST_MESSAGE = 'В ответ на это сообщение пришлите Ваш запрос (можно голосовым сообщением или текстом).'

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
            \n\
            \nОтблагодарить меня за инсайты можно переводом любой суммы на карты:\
            \nДля граждан России:\
            \n5469380092114452\
            \n\
            \nДля граждан других государств:\
            \n5269880013129754\
            \nIBAN $:\
            \nKZ30551B229777462USD\
            \n\
            \nIBAN€\
            \nKZ77551B229750110EUR\
            '''

SERVICES = {
    '3k' : text.K3,
    'family' : text.FAMILY,
    'cross' : text.CROSS,
    'stars' : text.STARS,
    'hourly' : text.HOURLY,
    'destiny' : text.DESTINY,
    'chakras' : text.CHAKRAS,
    'magic' : text.MAGIC,
    'relations' : text.RELATIONS,
    'pyramid' : text.PYRAMID,
}

SERVICES_NAMES = {
    '3k' : 'расклад 3к',
    'family' : 'родовой расклад',
    'cross' : 'кельтский крест',
    'stars' : 'астрологический расклад',
    'hourly' : 'личная консультация',
    'destiny' : 'консультация ПРЕДНАЗНАЧЕНИЕ',
    'chakras' : 'чакральный расклад',
    'magic' : 'магические способности',
    'relations' : 'отношения',
    'pyramid' : 'пирамида Исиды',
}