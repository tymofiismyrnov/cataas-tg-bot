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

redo_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
redo_btn1 = types.KeyboardButton("Repeat")
rebo_btn2 = types.KeyboardButton("Return to the menu")
