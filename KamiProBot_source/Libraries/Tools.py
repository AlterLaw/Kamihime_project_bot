import time
import cv2
import keyboard
import os
import sys
import numpy as np

import pyautogui

def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def check_for_f1():
    if keyboard.is_pressed('F1'):
        print("F1 key pressed. Terminating...")
        sys.exit()

def clicker(location,path):
    if location is not None:
        # Use the size of the template image found on screen
        template_width = cv2.imread(path).shape[1]
        template_height = cv2.imread(path).shape[0]
            
        center_x = location[0] + template_width // 2
        center_y = location[1] + template_height // 2
        pyautogui.click(center_x, center_y)
        time.sleep(3)

def search_single_on_array(image_paths, conf,tela):
    
    for path in image_paths:
        try:
            check_for_f1()
            template = cv2.imread(path)
            result = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= conf:
                return max_loc, path
            else:
                screenshot=None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1
        except Exception as e:
            print("Error on iteration over array")
            print(f"Error while processing image for path {path}: {e}")
        
    return None, None

def search_single_on_single(path,confidence,tela):
         
    try:
        check_for_f1()
            
        template = cv2.imread(path)
        result = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= confidence:
            return max_loc, path
        else:
            screenshot=None
            #print(f"Image not found for path: {path}. Skipping to the next image.")
            #sucess_counter=sucess_counter+1
    except Exception as e:
        print("Error on iteration over single")
        print(f"Error while processing image for path {path}: {e}")
        
    return None, None

def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_np

def stats_screen(process, max_value,min_value,Qcount,state):

    memory_info = process.memory_info()
    if memory_info> max_value:
        max_value = memory_info
    if memory_info < min_value:
        min_value = memory_info
    cpu_use = process.cpu_percent(interval=1)

    print("KamiPro bot running")
    print("---------------------")
    print("Hold F1 to cancel execution")
    print(f"Quests completed: {Qcount}")
    print(f"Current state: {state}")
    print(f"Used memory: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"Lowest record: {min_value.rss / 1024 / 1024:.2f} MB")
    print(f"Highest record: {max_value.rss / 1024 / 1024:.2f} MB")
    print(f"Used CPU: {cpu_use}%")
    print("---------------------")
    return max_value,min_value




