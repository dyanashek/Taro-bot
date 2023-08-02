# Telegram tarot cards bot
## Изменить язык: [Русский](README.md)
***
Telegram bot for automated collection of applications for the provision of services - transfers data filled in by the user to a google spreadsheet, sends a notification to the manager about the applications left.
## [LIVE](https://t.me/yakovleva_anna_taro_bot)
## [DEMO](README.demo.md)
## Functionality:
1. Collects information about the user
2. Checks if the application was left for the first time
3. Transfers user-filled data to google spreadsheets
4. Notifies the manager about abandoned applications, fixes unprocessed applications in the dialog
5. Colors in green the requests processed by the manager
6. Accepts payment confirmation, as well as a client request in text or audio format and sends it to the manager
## Commands:
**For convenience, it is recommended to add these commands to the side menu of the bot using [BotFather](https://t.me/BotFather).**
- menu - calls the menu (add via BotFather for convenient display)
- taro - request a service for deciphering the date of birth
- help - help

## Installation and use:
- Logging in case of an error is carried out in the file py_log.log
- Install dependencies:
```sh
pip install -r requirements.txt
```
- in the .env file specify:
   - Bot telegram token: **TELEGRAM_TOKEN**=TOKEN
   - Bot ID: **BOT_ID**=ID (first digits from bot token, before :)
   - Manager ID: **MANAGER_ID**=MANAGER_ID; will have the right to execute the /update command, he will receive notifications - to receive notifications, the manager needs to activate the bot from his account (press the "start" button)
   > To determine the user ID, you need to send any message from the corresponding account to the next [bot] (https://t.me/getmyid_bot). Value contained in **Your user ID** - User ID
   - Links to telegram channel and instagram **TELEGRAM_CHANNEL_LINK**, **INSTAGRAM_LINK**
   - Manager username - the "manager" button in the menu will enter the specified profile: **MANAGER_USERNAME**=example (specified without @)
- get file with credentials (connection parameters):\
https://console.cloud.google.com/ \
https://www.youtube.com/watch?v=bu5wXjz2KvU - instruction from 00:00 to 02:35\
Save the resulting file in the root of the project, with the name **service_account.json**
- provide service e-mail with access to the table (instruction in the video at the link above)
- set the following variables in the config.py file:\
**IMAGE_ID** - ID of the greeting image sent by the bot (to which it has access)\
**SPREAD_NAME** - the name of the table in google sheets where data about new applications is written\
**LIST_NAME** - sheet name in the table
- run the project:
```sh
python3 main.py
```
## Recommendations for use:
- before activating the bot, be sure to set the names of the columns for easy navigation and correct operation:
     - order of displayed information on the application sheet:
         1. unique user ID
         2. user nickname in Telegram
         3. username
         4. last name of the user
         5. user's instagram link
         6. date of birth of the user
         7. time of sending the application (Moscow)