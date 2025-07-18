from telebot import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from res.scr.ops import *

apihelper.READ_TIMEOUT = 60  
apihelper.CONNECT_TIMEOUT = 30  
apihelper.RETRY_ON_ERROR = True  
apihelper.MAX_RETRIES = 3  

CONF_PATH = "res/conf/conf.json"
API = open("API.txt", "r", encoding="utf-8").read().split()[0]
ADMINS = [1433192741, 880031561]

configures = read_json(CONF_PATH)
# print(configures)

mariaconnection = MariaConnection(args=configures["database"])
users = Users(mariaconnection)

bot = TeleBot(API)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    online_lyc = InlineKeyboardButton(text="Тг канал Лицея Онлайн", url="https://t.me/hselyc_online")
    lyc = InlineKeyboardButton(text="Тг канал Большого Лицея", url="https://t.me/lyceumhse")
    ready = InlineKeyboardButton(text="Готово!", callback_data="ready")

    keyboard.add(online_lyc)
    keyboard.add(lyc)
    keyboard.add(ready)

    bot.send_message(message.chat.id, text=configures["phrazes"]["start"], reply_markup=keyboard)

    if users.get_by_username(message.chat.username) != None:
        users.insert_with_username(message.chat.username, message.chat.id, "NO_EMAIL")

    # else:
    #     bot.send_message(message.chat.id, text=configures["phrazes"]["email"])
    #     bot.register_next_step_handler_by_chat_id(message.chat.id, email)
    

        
# def email(message):
#     if "@" in message.text:
#         users.insert_with_username(message.chat.username, message.chat.id, message.text)
#         bot.send_message(message.chat.id, text=configures["phrazes"]["correct-email"])
#         bot.send_message(message.chat.id, text=configures["materials"]["materials"])

#     else:
#         bot.send_message(message.chat.id, text=configures["phrazes"]["incorrect-email"])
#         bot.send_message(message.chat.id, text=configures["phrazes"]["email"])
#         bot.register_next_step_handler_by_chat_id(message.chat.id, email)

# @bot.message_handler(commands=["game"])
# def game(message):
#     keyboard = InlineKeyboardMarkup()

#     for theme in configures["paths"]:
#         btn = InlineKeyboardButton(text=theme, callback_data=theme)
#         keyboard.add(btn)
    
#     bot.send_message(message.chat.id, text=configures["phrazes"]["game"], reply_markup=keyboard)
        
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.data in configures["paths"].keys():
#         keyboard = InlineKeyboardMarkup()

#         for level in configures["paths"][call.data]:
#             btn = InlineKeyboardButton(text=level, callback_data=f"{call.data}_{level}")
#             keyboard.add(btn)

#         bot.send_message(call.message.chat.id, text=configures["phrazes"]["level"], reply_markup=keyboard)
    
#     elif "_" in call.data:
#         path = call.data.split(sep="_")
#         photo = open(configures["pngs"] + configures["paths"][path[0]][path[1]], "rb")
#         bot.send_photo(call.message.chat.id, photo=photo)
#         photo.close()

        
def email(message):
    if "@" in message.text:
        users.change_email(message.chat.username, message.text)
        bot.send_message(message.chat.id, text=configures["phrazes"]["correct-email"])

    else:
        bot.send_message(message.chat.id, text=configures["phrazes"]["incorrect-email"])
        bot.send_message(message.chat.id, text=configures["phrazes"]["email2"])
        bot.register_next_step_handler_by_chat_id(message.chat.id, email)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "ready":
        bot.send_message(call.message.chat.id, text=configures["phrazes"]["email"])
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, callback=email)




@bot.message_handler(commands=["admin"])
def admin(message):
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, text=configures["phrazes"]["admin"])
        bot.register_next_step_handler_by_chat_id(message.chat.id, admin_forward)


def admin_forward(message):
    # print(users.get_all_telegramms())
    for user_id in users.get_all_telegramms():
        # print(user_id)
        try:
            bot.copy_message(
            chat_id=int(user_id[0]),
            from_chat_id=message.chat.id,
            message_id=message.message_id
            )
            continue
        except Exception as e:
            print(e)


# @bot.message_handler(commands=["materials"])
# def materials(message):
#     bot.send_message(message.chat.id, text=configures["materials"]["materials"])


# @bot.message_handler(commands=["materials"])
# def materials(message):
#     bot.send_message(message.chat.id, text=configures["phrazes"]["materials_pw"])
#     bot.register_next_step_handler_by_chat_id(message.chat.id, send_materials)

# def send_materials(message):
#     if str(message.text) == str(configures["materials"]["password"]):
#         bot.send_message(message.chat.id, text=configures["materials"]["materials"])
#     else:
#         bot.send_message(message.chat.id, text=configures["phrazes"]["incorrect_materials_pw"])


if __name__ == "__main__":
    bot.polling(60)