import psutil
from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import numpy as np
import Libraries.img_arraysV3 as imgV3
import pyautogui
import time
import sys
import cv2

# Arbitrary variables
confidence_level = 0.9
max_attempts = 2
retry_interval = 1

paths=imgV3.screen_elements()

# Replace 'path/to/your/image.png' with the path to your image file
image_paths = [
    paths["item"],
    paths["confirm"],
    paths["retry"],
    paths["my_supp"],
    paths["to_quest"],
    paths["start_battle"],
    paths["burst"],
    
]


def find_image_on_screen(image_paths, confidence):
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    for path in image_paths:
        try:
            
            
            template = cv2.imread(path)
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                return max_loc, path
                

        except Exception as e:
            print(f"Error while processing image for path {path}: {e}")
    return None, None
        
        

    #print("Exceeded max attempts for all images. No image found.")
    return None

def stats_screen(params):

    print("KamiPro bot running")
    print("---------------------")
    print("Hold F1 to cancel execution")
    print(f"Quests completed: {params[3]}")
    memory_info = params[0].memory_info()
    print(f"Used memory: {memory_info.rss / 1024 / 1024:.2f} MB")

    if memory_info> params[2]:
        params[2] = memory_info
    if memory_info <params[1]:
        params[1] = memory_info
    
    print(f"Lowest record: {params[1].rss / 1024 / 1024:.2f} MB")
    print(f"Highest record: {params[2].rss / 1024 / 1024:.2f} MB")


    #cpu_use = process.cpu_percent(interval=1)
    #print(f"Used CPU: {cpu_use}%")
    print("---------------------")

    

def find_and_click(image_paths, confidence):
    
    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")

    current_process = psutil.Process()
    lowest_record= current_process.memory_info()
    highest_record = current_process.memory_info()
    quests_completed_counter=0
    
    params= [
        current_process,
        lowest_record,
        highest_record,
        quests_completed_counter,
        ]
    running = True

    while running:

        tools.clear_console()
        #stats_screen(params)
        tools.check_for_f1()
        
        location, path = find_image_on_screen(image_paths, confidence)
        #print(location)
        #print(path)

        if location is not None:
            # Use the size of the template image found on screen
            if path ==paths["retry"]:
                params[3]+=1
                    
            if path ==paths["burst"] or path is None:
                time.sleep(5)
            else:
                template_width = cv2.imread(image_paths[0]).shape[1]
                template_height = cv2.imread(image_paths[0]).shape[0]
                center_x = location[0] + template_width // 2
                center_y = location[1] + template_height // 2
                pyautogui.click(center_x, center_y)


#            if params[3]==10:
#               running=False


        tools.check_for_f1()
        time.sleep(1)

        



if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    # Instance
    # relatorio_erro = log.MemoryLogger()
    # sys.stdout = relatorio_erro

    # Call the function with the specified image path and confidence level
    find_and_click(image_paths, confidence_level)

    # Restore sys.stdout to the original state
    # sys.stdout = sys.__stdout__
