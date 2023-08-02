from telebot import types

import config

def main_keyboard():
    """Generates main keyboard that have option of filling form, check instagram."""

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('💰 Услуги и стоимость', callback_data = f'services'))
    keyboard.add(types.InlineKeyboardButton('🆓 Бесплатно', callback_data = f'free'))
    keyboard.add(types.InlineKeyboardButton('🎴 Расшифровка д/р за ДОНАТ', callback_data = f'donate'))
    keyboard.add(types.InlineKeyboardButton('🌟 Астрорасклад', callback_data = f'service_stars'))
    keyboard.add(types.InlineKeyboardButton('⏰ Часовая консультация', callback_data = f'service_hourly'))
    keyboard.add(types.InlineKeyboardButton('🌏Консультация Предназначение', callback_data = f'service_destiny'))
    keyboard.add(types.InlineKeyboardButton('💎 Телеграмм канал', url = config.TELEGRAM_CHANNEL_LINK))
    keyboard.add(types.InlineKeyboardButton('🔗 Instagram', url = config.INSTAGRAM_LINK))

    return keyboard


def services_keyboard():
    """Generates keyboard with main services."""

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('3️⃣ Расклад 3к', callback_data = f'service_3k'))
    keyboard.add(types.InlineKeyboardButton('👨‍👩‍👧‍👦 Родовой расклад', callback_data = f'service_family'))
    keyboard.add(types.InlineKeyboardButton('⬜️ Кельтский крест', callback_data = f'service_cross'))
    keyboard.add(types.InlineKeyboardButton('🌟 Астрологический расклад', callback_data = f'service_stars'))
    keyboard.add(types.InlineKeyboardButton('⏰ Личная консультация', callback_data = f'service_hourly'))
    keyboard.add(types.InlineKeyboardButton('🌏 Консультация Предназначение', callback_data = f'service_destiny'))
    keyboard.add(types.InlineKeyboardButton('⌛️ Чакральный', callback_data = f'service_chakras'))
    keyboard.add(types.InlineKeyboardButton('🧿 Магические способности', callback_data = f'service_magic'))
    keyboard.add(types.InlineKeyboardButton('🧡 Отношения', callback_data = f'service_relations'))
    keyboard.add(types.InlineKeyboardButton('🌙 Пирамида Исиды', callback_data = f'service_pyramid'))
    keyboard.add(types.InlineKeyboardButton('🏡 Главное меню', callback_data = f'main'))

    return keyboard


def pay_keyboard(service):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('💰 Оплачено', callback_data = f'paid_{service}'))
    keyboard.add(types.InlineKeyboardButton('🏡 Главное меню', callback_data = f'main'))

    return keyboard


def paid_keyboard():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🙋‍♀️ Связаться со мной', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    keyboard.add(types.InlineKeyboardButton('🏡 Главное меню', callback_data = f'main'))

    return keyboard


def menu_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🏡 Главное меню', callback_data = f'main'))
    return keyboard


def taro_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🎴 Получить расшифровку', callback_data = f'taro'))
    keyboard.add(types.InlineKeyboardButton('🏡 Главное меню', callback_data = f'main'))

    return keyboard


def manager_keyboard():
    """Generates keyboard with only 'connect with manager' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🙋‍♀️ Записаться на расклад', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    return keyboard


def enter_name_keyboard():
    """Makes a reply to a message that asks about the name."""
    return types.ForceReply(input_field_placeholder='Введите Ваше имя')


def enter_family_name_keyboard():
    """Makes a reply to a message that asks about the family name."""
    return types.ForceReply(input_field_placeholder='Введите Вашу фамилию')


def enter_instagram_keyboard():
    """Makes a reply to a message that asks about instagram link."""
    return types.ForceReply(input_field_placeholder='Введите Ваш instagram')


def enter_birthday_keyboard():
    """Makes a reply to a message that asks about birthday."""
    return types.ForceReply(input_field_placeholder='дд.мм.гггг')


def enter_check_keyboard():
    return types.ForceReply(input_field_placeholder='Чек об оплате')

def enter_photo_keyboard():
    return types.ForceReply(input_field_placeholder='Ваше селфи')

def enter_request_keyboard():
    return types.ForceReply(input_field_placeholder='Ваш запрос')


def confirm_first_name_keyboard(first_name):
    """Generates keyboard with 'confirm name' and self input options."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_name_{first_name}'))
    keyboard.add(types.InlineKeyboardButton('🖋 Ввести вручную', callback_data = f'enter_name'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel'))
    return keyboard


def confirm_family_name_keyboard(family_name):
    """Generates keyboard with 'confirm name' and self input options."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_family_{family_name}'))
    keyboard.add(types.InlineKeyboardButton('🖋 Ввести вручную', callback_data = f'enter_family'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel'))
    return keyboard


def confirm_form_keyboard(birthday):
    """Generates keyboard to confirm information fo filling form."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Отправить на расшифровку', callback_data = f'fill_{birthday}'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel'))
    return keyboard


def mark_as_complete(user_id):
    """Generates button that marks message as completed."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Выполнено', callback_data = f'complete_{user_id}'))
    return keyboard