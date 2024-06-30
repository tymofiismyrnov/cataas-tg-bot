import telebot
from telebot import types
import requests
import os
from keyboards import menu_kb, main_kb, color_kb

description_text = """
This bot returns a random cat picture or gif, or a picture with text that you type in.

Bot uses https://cataas.com/ API, authored by https://twitter.com/kevinbalicot

Source: https://github.com/tymofiismyrnov/cataas-tg-bot
Feel free to contribute

Run /start to begin
"""

bot = telebot.TeleBot(os.getenv("TG_BOT_TOKEN"))
bot.set_my_description(description_text)
bot.set_my_short_description("Get a random cat pic with your text")


chats = {}


@bot.message_handler(commands=["start", "help", "menu"])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "Welcome to the *cat as a service* bot, press the menu button below to start",
        reply_markup=menu_kb,
        parse_mode="Markdown",
    )


@bot.message_handler(func=lambda message: message.text == "☰ Menu")
def menu(message):
    bot.send_message(message.chat.id, "Select an option 👇", reply_markup=main_kb)


@bot.message_handler(func=lambda message: message.text == "Picture")
def send_random_cat_pic(message):
    try:
        response = requests.get("https://cataas.com/cat")
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat picture. Please try again."
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


@bot.message_handler(func=lambda message: message.text == "Gif")
def send_random_cat_gif(message):
    bot.send_message(message.chat.id, "Getting your gif. Wait a second please...")
    try:
        response = requests.get("https://cataas.com/cat/gif")
        if response.status_code == 200:
            with open("cat.gif", "wb") as file:
                file.write(response.content)
            with open("cat.gif", "rb") as file:
                bot.send_animation(message.chat.id, file)
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat gif. Please try again."
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


@bot.message_handler(
    func=lambda message: message.text in ["Picture with text", "Gif with text"]
)
def prompt_cat_saying(message):
    if message.chat.id not in chats:
        chats[message.chat.id] = {}

    if message.text == "Picture with text":
        request_type = "pic"
    else:
        request_type = "gif"

    chats[message.chat.id] = {"type": request_type}
    bot.send_message(
        message.chat.id,
        "Please enter the text you want the cat to say:",
        reply_markup=main_kb,
    )
    bot.register_next_step_handler(message, choose_color)


def choose_color(message):
    chats[message.chat.id]["text"] = message.text
    bot.send_message(
        message.chat.id, "Choose a color for the text:", reply_markup=color_kb
    )


@bot.message_handler(func=lambda message: message.text in ["Black", "White"])
def send_cat_saying(message):
    user_text = chats[message.chat.id].get("text")
    color = message.text.lower()
    request_type = chats[message.chat.id].get("type")

    if request_type == "gif":
        bot.send_message(message.chat.id, "Getting your gif. Wait a second please...")
        endpoint = (
            f"https://cataas.com/cat/gif/says/{user_text}?fontColor={color}&fontSize=50"
        )
    else:
        endpoint = (
            f"https://cataas.com/cat/says/{user_text}?fontColor={color}&fontSize=50"
        )
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            if request_type == "gif":
                with open("cat_saying.gif", "wb") as file:
                    file.write(response.content)
                with open("cat_saying.gif", "rb") as file:
                    bot.send_animation(message.chat.id, file, reply_markup=main_kb)
            else:
                bot.send_photo(message.chat.id, response.content, reply_markup=main_kb)
        else:
            bot.send_message(
                message.chat.id,
                "Failed to fetch cat saying. Please try again.",
                reply_markup=main_kb,
            )
    except Exception as e:
        bot.send_message(
            message.chat.id, f"An error occurred: {e}", reply_markup=main_kb
        )


if __name__ == "__main__":
    bot.infinity_polling()
