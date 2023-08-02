import datetime

def verify_instagram_link(text):
    text = text.replace(' ', '')
    if ('https://instagram.com/') in text and len('https://instagram.com/') < len(text):
        return text
    return False

def verify_birthday(text):
    birthday = text.replace(' ', '').replace('\\', '.').replace('/', '.').replace('-', '.').replace('_', '.').replace(',', '.')
    try:
        birthday_date = datetime.datetime.strptime(birthday, '%d.%m.%Y').date() 

        if birthday_date > (datetime.datetime.utcnow() + datetime.timedelta(days=1)).date():
            return False
        
    except:
        return False
    
    return birthday
