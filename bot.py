import telebot
from telebot import types
import requests
import os
import logging
from keyboards import menu_kb, main_kb, color_kb, post_gen_kb

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
    logger.info(
        f"Received {message.text} command from user {message.chat.id} ({message.chat.username})"
    )
    bot.send_message(
        message.chat.id,
        "Welcome to the *cat as a service* bot, press the menu button below to start",
        reply_markup=menu_kb,
        parse_mode="Markdown",
    )


@bot.message_handler(func=lambda message: message.text == "☰ Menu")
def menu(message):
    logger.info(f"User {message.chat.id} ({message.chat.username}) opened the menu")
    bot.send_message(message.chat.id, "Select an option 👇", reply_markup=main_kb)


@bot.message_handler(func=lambda message: message.text == "Picture")
def send_random_cat_pic(message):
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) requested a random cat picture"
    )
    try:
        response = requests.get("https://cataas.com/cat")
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
            logger.info(
                f"Sent a random cat picture to user {message.chat.id} ({message.chat.username})"
            )
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat picture. Please try again."
            )
            logger.error(
                f"Failed to fetch cat picture for user {message.chat.id} ({message.chat.username})"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")
        logger.error(
            f"An error occurred while fetching cat picture for user {message.chat.id} ({message.chat.username}): {e}"
        )


@bot.message_handler(func=lambda message: message.text == "Gif")
def send_random_cat_gif(message):
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) requested a random cat gif"
    )
    bot.send_message(message.chat.id, "Getting your gif. Just a sec...")
    try:
        response = requests.get("https://cataas.com/cat/gif")
        if response.status_code == 200:
            file_path = f"cat_{message.chat.id}.gif"
            with open(file_path, "wb") as file:
                file.write(response.content)
            with open(file_path, "rb") as file:
                bot.send_animation(message.chat.id, file)
            os.remove(file_path)  # Delete the file after sending
            logger.info(
                f"Sent a random cat gif to user {message.chat.id} ({message.chat.username})"
            )
        else:
            bot.send_message(
                message.chat.id, "Failed to fetch cat gif. Please try again."
            )
            logger.error(
                f"Failed to fetch cat gif for user {message.chat.id} ({message.chat.username})"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")
        logger.error(
            f"An error occurred while fetching cat gif for user {message.chat.id} ({message.chat.username}): {e}"
        )


@bot.message_handler(
    func=lambda message: message.text in ["Picture with text", "Gif with text"]
)
def prompt_cat_saying(message):
    if message.chat.id not in chats:
        chats[message.chat.id] = {}

    request_type = "pic" if message.text == "Picture with text" else "gif"
    chats[message.chat.id] = {"type": request_type}

    bot.send_message(
        message.chat.id,
        "Please enter the text you want the cat to say:",
        reply_markup=main_kb,
    )
    bot.register_next_step_handler(message, choose_color)
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) is prompted to enter text for {request_type}"
    )


def choose_color(message):
    chats[message.chat.id]["text"] = message.text
    bot.send_message(
        message.chat.id, "Choose a color for the text:", reply_markup=color_kb
    )
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) entered text: {message.text}"
    )


@bot.message_handler(func=lambda message: message.text in ["Black", "White"])
def set_color_and_generate(message):
    chats[message.chat.id]["color"] = message.text.lower()
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) chose color: {message.text}"
    )
    send_cat_saying(message)



def send_cat_saying(message):
    user_text = chats[message.chat.id].get("text")
    color = chats[message.chat.id].get("color")
    request_type = chats[message.chat.id].get("type")

    if request_type == "gif":
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
                bot.send_message(message.chat.id, "Getting your gif. Just a sec...")
                file_path = f"cat_saying_{message.chat.id}.gif"
                with open(file_path, "wb") as file:
                    file.write(response.content)
                with open(file_path, "rb") as file:
                    bot.send_animation(message.chat.id, file, reply_markup=post_gen_kb)
                os.remove(file_path)
            else:
                bot.send_photo(
                    message.chat.id, response.content, reply_markup=post_gen_kb
                )

            logger.info(
                f"Sent {request_type} with text to user {message.chat.id} ({message.chat.username})"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Failed to fetch cat saying. Please try again.",
                reply_markup=main_kb,
            )
            logger.error(
                f"Failed to fetch {request_type} with text for user {message.chat.id} ({message.chat.username})"
            )
    except Exception as e:
        bot.send_message(
            message.chat.id, f"An error occurred: {e}", reply_markup=main_kb
        )
        logger.error(
            f"An error occurred while fetching {request_type} with text for user {message.chat.id} ({message.chat.username}): {e}"
        )


@bot.message_handler(func=lambda message: message.text == "Try Again")
def try_again(message):
    if message.chat.id in chats:
        logger.info(
            f"User {message.chat.id} ({message.chat.username}) chose to try again"
        )
        send_cat_saying(message)



@bot.message_handler(func=lambda message: message.text == "Main Menu")
def return_to_main_menu(message):
    bot.send_message(message.chat.id, "Select an option 👇", reply_markup=main_kb)
    logger.info(
        f"User {message.chat.id} ({message.chat.username}) returned to the main menu"
    )


if __name__ == "__main__":
    bot.infinity_polling()
