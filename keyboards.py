from telebot import types

import config

def main_keyboard():
    """Generates main keyboard that have option of filling form, check instagram."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🎴 Получить расшифровку', callback_data = f'taro'))
    keyboard.add(types.InlineKeyboardButton('🙋‍♀️ Записаться на расклад', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    keyboard.add(types.InlineKeyboardButton('💎 Телеграмм канал', url = config.TELEGRAM_CHANNEL_LINK))
    keyboard.add(types.InlineKeyboardButton('🔗 Instagram', url = config.INSTAGRAM_LINK))
    return keyboard

def manager_keyboard():
    """Generates keyboard with only 'connect with manager' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🙋‍♀️ Записаться на расклад', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    return keyboard

def enter_name_keyboard():
    """Makes a reply to a message that asks about the name."""
    return types.ForceReply(input_field_placeholder=f'Введите Ваше имя')

def enter_family_name_keyboard():
    """Makes a reply to a message that asks about the family name."""
    return types.ForceReply(input_field_placeholder=f'Введите Вашу фамилию')

def enter_instagram_keyboard():
    """Makes a reply to a message that asks about instagram link."""
    return types.ForceReply(input_field_placeholder=f'Введите Ваш instagram')

def enter_birthday_keyboard():
    """Makes a reply to a message that asks about birthday."""
    return types.ForceReply(input_field_placeholder=f'дд.мм.гггг')

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