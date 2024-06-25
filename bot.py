import telebot
from telebot import types
import requests
import os

bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Picture")
btn2 = types.KeyboardButton("Gif")
btn3 = types.KeyboardButton("Picture with text")
markup.row(btn1, btn2)
markup.row(btn3)

chats = {}

print(chats)

@bot.message_handler(commands=['start', 'help', 'menu'])
def menu(message):
    bot.send_message(
        message.chat.id, "Select an option in the menu below 👇", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Picture")
def send_random_cat_pic(message):
    try:
        response = requests.get("https://cataas.com/cat")
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat picture. Please try again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


@bot.message_handler(func=lambda message: message.text == "Gif")
def send_random_cat_gif(message):
    bot.send_message(
        message.chat.id, "Fetching a gif....this might take a couple of seconds")
    try:
        response = requests.get("https://cataas.com/cat/gif")
        if response.status_code == 200:
            with open("cat.gif", "wb") as file:
                file.write(response.content)
            with open("cat.gif", "rb") as file:
                bot.send_animation(message.chat.id, file)
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat gif. Please try again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


@bot.message_handler(func=lambda message: message.text == "Picture with text")
def prompt_cat_saying(message):
    chats[message.chat.id] = {}
    print(chats)
    bot.send_message(
        message.chat.id, "Please enter the text you want the cat to say:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_color)


def choose_color(message):
    chats[message.chat.id]['text'] = message.text
    print(chats)
    markup_inline = types.InlineKeyboardMarkup()
    btn_black = types.InlineKeyboardButton("Black", callback_data="black")
    btn_white = types.InlineKeyboardButton("White", callback_data="white")
    markup_inline.add(btn_black, btn_white)
    bot.send_message(
        message.chat.id, "Choose a color for the text:", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def send_cat_saying(call):
    user_text = chats[call.message.chat.id]['text']
    color = call.data
    try:
        response = requests.get(
            f"https://cataas.com/cat/says/{user_text}?fontColor={color}&fontSize=50")
        if response.status_code == 200:
            bot.send_photo(call.message.chat.id,
                           response.content, reply_markup=markup)
        else:
            bot.send_message(
                call.message.chat.id, "Failed to fetch cat saying. Please try again.", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {
                         e}", reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
