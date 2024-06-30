import telebot
from telebot import types


menu_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_btn1 = types.KeyboardButton("☰ Menu")
menu_kb.row(menu_btn1)

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Picture")
btn2 = types.KeyboardButton("Gif")
btn3 = types.KeyboardButton("Picture with text")
btn4 = types.KeyboardButton("Gif with text")
main_kb.row(btn1, btn2)
main_kb.row(btn3, btn4)

color_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
color_btn1 = types.KeyboardButton("Black")
color_btn2 = types.KeyboardButton("White")
color_kb.row(color_btn1, color_btn2)

post_gen_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_try_again = types.KeyboardButton("Try Again")
btn_main_menu = types.KeyboardButton("Main Menu")
post_gen_kb.row(btn_try_again, btn_main_menu)

