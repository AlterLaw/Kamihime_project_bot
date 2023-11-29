import os
import sys

import keyboard

def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def check_for_f1():
    if keyboard.is_pressed('F1'):
        print("F1 key pressed. Terminating...")
        sys.exit()





