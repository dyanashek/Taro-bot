import telebot
import logging
import datetime
import threading

import config
import text
import utils
import functions
import keyboards

logging.basicConfig(level=logging.ERROR, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_photo(chat_id=message.chat.id,
                   photo=config.MENU_IMAGE,
                   reply_markup=keyboards.main_keyboard(),
                   )
    

@bot.message_handler(commands=['taro'])
def start_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_username = message.from_user.username

    # the flag that indicates does user allowed to fill form
    fill_form_flag = False

    # gets information about user from database
    user = functions.is_new_user(user_id)

    # if there isn't any information
    if user == []:
        # adding user to database, change flag
        functions.add_user(user_id, user_username)
        fill_form_flag = True
    
    # if user already in database
    else:
        # check has he filled up the form to the end
        form_filled = functions.is_form_filled(user)

        # if he doesn't, delete previous information, change flag
        if not form_filled:
            functions.set_to_none(user_id)
            fill_form_flag = True
        
        # if he does - inform that only one filling is available
        else:
            bot.send_message(chat_id=chat_id,
                            text=config.FILLED_MESSAGE,
                            reply_markup=keyboards.manager_keyboard(),
                            parse_mode='Markdown',
                            )
            
    # if user allowed to fill the form
    if fill_form_flag:
        first_name = message.from_user.first_name
        reply_text, keyboard = functions.name_response(first_name)

        bot.send_message(chat_id=chat_id,
                            text=reply_text,
                            reply_markup=keyboard,
                            parse_mode='Markdown',
                            )
            

@bot.message_handler(commands=['menu'])
def start_message(message):
    bot.send_photo(chat_id=message.chat.id,
                   photo=config.IMAGE_ID,
                   reply_markup=keyboards.main_keyboard(),
                   parse_mode='MarkdownV2',
                   )


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text=text.HELP,
                     parse_mode='Markdown',
                     )
    

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_username = call.from_user.username

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'taro':
        # the flag that indicates does user allowed to fill form
        fill_form_flag = False

        # gets information about user from database
        user = functions.is_new_user(user_id)

        # if there isn't any information
        if user == []:
            # adding user to database, change flag
            functions.add_user(user_id, user_username)
            fill_form_flag = True
        
        # if user already in database
        else:
            # check has he filled up the form to the end
            form_filled = functions.is_form_filled(user)

            # if he doesn't, delete previous information, change flag
            if not form_filled:
                functions.set_to_none(user_id)
                fill_form_flag = True
            
            # if he does - inform that only one filling is available
            else:
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass

                bot.send_message(chat_id=chat_id,
                                  text=config.FILLED_MESSAGE,
                                  reply_markup=keyboards.manager_keyboard(),
                                  parse_mode='Markdown',
                                  )
                
        # if user allowed to fill the form
        if fill_form_flag:
            first_name = call.from_user.first_name
            reply_text, keyboard = functions.name_response(first_name)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                                text=reply_text,
                                reply_markup=keyboard,
                                parse_mode='Markdown',
                                )
    
    elif query == 'donate':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        bot.send_photo(chat_id=chat_id,
                   photo=config.IMAGE_ID,
                   caption=config.MAIN_TEXT,
                   reply_markup=keyboards.taro_keyboard(),
                   parse_mode='MarkdownV2',
                   )

    
    elif query == 'services':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id,
                         text=text.SERVICES,
                         reply_markup=keyboards.services_keyboard(),
                         parse_mode='Markdown',
                         )
    
    elif query == 'service':
        service = call_data[1]

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id,
                         text=config.SERVICES[service],
                         reply_markup=keyboards.pay_keyboard(service),
                         parse_mode='Markdown',
                         )
    
    elif query == 'free':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id,
                         text=text.FREE,
                         reply_markup=keyboards.menu_keyboard(),
                         parse_mode='Markdown',
                         disable_web_page_preview=True,
                         )

    elif query == 'paid':
        service = call_data[1]
        if user_username:
            if functions.is_new_user(user_id):
                functions.update_username(user_id, user_username)
            else:
                functions.add_user(user_id, user_username)
                
            functions.update_service(user_id, service)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                             text=config.CHECK_MESSAGE,
                             reply_markup=keyboards.enter_check_keyboard(),
                             )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.NO_USERNAME,
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pay_keyboard(service),
                                          )

    elif query == 'confirm':
        info_category = call_data[1]
        info = call_data[2]

        functions.fill_form_info(info_category=info_category,
                                 info=info,
                                 user_id=user_id,
                                 )
        
        if info_category == 'family':
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                     text=config.INSTAGRAM_MESSAGE,
                     parse_mode='Markdown',
                     reply_markup=keyboards.enter_instagram_keyboard(),
                     )

        elif info_category == 'name':
            family_name = call.from_user.last_name
            reply_text, keyboard = functions.family_name_response(family_name)
            
            # if user hasn't family name in profile
            if reply_text == config.FAMILY_NAME_MESSAGE:
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass
                
                bot.send_message(chat_id=chat_id,
                     text=reply_text,
                     parse_mode='Markdown',
                     reply_markup=keyboard,
                     )
            
            # if user has family name in profile
            else:
                bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=reply_text,
                                  parse_mode='Markdown',
                                  )
                
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboard,
                                            )

    elif query == 'enter':
        info_category = call_data[1]

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        
        reply_text, keyboard = functions.enter_response(info_category)

        bot.send_message(chat_id=chat_id,
                     text=reply_text,
                     parse_mode='Markdown',
                     reply_markup=keyboard,
                     )
    
    elif query == 'fill':
        birthday = datetime.datetime.strptime(call_data[1], '%d.%m.%Y').date() 
        functions.fill_form_info(info_category='birth',
                                 info=birthday,
                                 user_id=user_id,
                                 )

        threading.Thread(daemon=True, 
                         target=functions.transfer_to_google_sheets,
                         args=(user_id,),
                         ).start()
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id,
                     text=config.FINAL_MESSAGE,
                     parse_mode='MarkdownV2',
                     reply_markup=keyboards.manager_keyboard(),
                     )
        
        threading.Thread(daemon=True, 
                         target=functions.notify_manager,
                         args=(user_id,),
                         ).start()

    elif query == 'complete':
        user_id = call_data[1]

        bot.unpin_chat_message(chat_id=chat_id,
                               message_id=message_id,
                               )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )
        
        threading.Thread(daemon=True, 
                         target=functions.color_spread,
                         args=(user_id,),
                         ).start()
        
        
    # cancel the action, deletes keyboard and changes message
    elif query == 'cancel':
        bot.edit_message_text(message_id=message_id,
                            chat_id=chat_id,
                            text=config.CANCEL_MESSAGE,
                            )     
        
    elif query == 'main':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_photo(chat_id=chat_id,
                   photo=config.MENU_IMAGE,
                   reply_markup=keyboards.main_keyboard(),
                   )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with type text."""

    if (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID) and\
    message.reply_to_message.text == config.REQUEST_MESSAGE:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.reply_to_message.id
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        functions.update_request(user_id, message.text, 'text')

        threading.Thread(daemon=True, 
                         target=functions.handle_payment,
                         args=(user_id,),
                         ).start()

        bot.send_message(chat_id=chat_id,
                             text=text.PAID,
                             reply_markup=keyboards.paid_keyboard(),
                             )

    elif (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID):
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.reply_to_message.id

        info_category = ''
        for keyword in config.INFO_CATEGORY_IDENTIFIER:
            if keyword in message.reply_to_message.text:
                info_category = config.INFO_CATEGORY_IDENTIFIER[keyword]
                break

        if info_category == 'name':
            functions.fill_form_info(info_category=info_category,
                                     info=message.text,
                                     user_id=user_id,
                                     )
            
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass
            
            bot.send_message(chat_id=chat_id,
                     text=config.FAMILY_NAME_MESSAGE,
                     parse_mode='Markdown',
                     reply_markup=keyboards.enter_family_name_keyboard(),
                     )
        
        elif info_category == 'family':
            functions.fill_form_info(info_category=info_category,
                                     info=message.text,
                                     user_id=user_id,
                                     )
            
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass
            
            bot.send_message(chat_id=chat_id,
                     text=config.INSTAGRAM_MESSAGE,
                     parse_mode='Markdown',
                     reply_markup=keyboards.enter_instagram_keyboard(),
                     )
            
        elif info_category == 'instagram':
            instagram_link = utils.verify_instagram_link(message.text)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            if instagram_link:
                functions.fill_form_info(info_category=info_category,
                                        info=instagram_link,
                                        user_id=user_id,
                                        )
            
                bot.send_message(chat_id=chat_id,
                        text=config.BIRTHDAY_MESSAGE,
                        parse_mode='Markdown',
                        reply_markup=keyboards.enter_birthday_keyboard(),
                        )
                
            else:
                bot.send_message(chat_id=chat_id,
                        text=config.WRONG_FORMAT_MESSAGE + config.INSTAGRAM_MESSAGE,
                        parse_mode='Markdown',
                        reply_markup=keyboards.enter_instagram_keyboard(),
                        )
                
        elif info_category == 'birth':
            birthday = utils.verify_birthday(message.text)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            if birthday:
                user_info = functions.is_new_user(user_id)

                first_name = user_info[3]
                family_name = user_info[4]
                instagram_link = user_info[5]
                
                reply_text = functions.confirm_form_reply(name=first_name,
                                                          family_name=family_name,
                                                          instagram_link=instagram_link,
                                                          birthday=birthday,
                                                          )

                bot.send_message(chat_id=chat_id,
                                 text=reply_text,
                                 reply_markup=keyboards.confirm_form_keyboard(birthday),
                                 parse_mode='Markdown',
                                 )

            else:
                bot.send_message(chat_id=chat_id,
                        text=config.WRONG_FORMAT_MESSAGE + config.BIRTHDAY_MESSAGE,
                        parse_mode='Markdown',
                        reply_markup=keyboards.enter_birthday_keyboard(),
                        )


@bot.message_handler(content_types=['document'])
def handle_voice(message):

    if (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID) and\
    message.reply_to_message.text == config.CHECK_MESSAGE:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.reply_to_message.id
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        functions.update_check(user_id, message.document.file_id, 'document')

        bot.send_message(chat_id=chat_id,
                             text=config.PHOTO_MESSAGE,
                             reply_markup=keyboards.enter_photo_keyboard(),
                             )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print(message)
    if (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID):
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.reply_to_message.id

        if message.reply_to_message.text == config.CHECK_MESSAGE:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            functions.update_check(user_id, message.photo[-1].file_id, 'photo')

            bot.send_message(chat_id=chat_id,
                             text=config.PHOTO_MESSAGE,
                             reply_markup=keyboards.enter_photo_keyboard(),
                             )
        
        elif message.reply_to_message.text == config.PHOTO_MESSAGE:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            functions.update_photo(user_id, message.photo[-1].file_id)

            bot.send_message(chat_id=chat_id,
                             text=config.REQUEST_MESSAGE,
                             reply_markup=keyboards.enter_request_keyboard(),
                             )


@bot.message_handler(content_types=['voice'])
def handle_voice(message):

    if (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID) and\
    message.reply_to_message.text == config.REQUEST_MESSAGE:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.reply_to_message.id
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        functions.update_request(user_id, message.voice.file_id, 'voice')

        threading.Thread(daemon=True, 
                         target=functions.handle_payment,
                         args=(user_id,),
                         ).start()
        
        bot.send_message(chat_id=chat_id,
                             text=text.PAID,
                             reply_markup=keyboards.paid_keyboard(),
                             )


if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass
