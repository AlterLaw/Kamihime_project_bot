from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import numpy as np
import pyautogui
import time
import sys
import cv2

# Arbitrary variables
confidence_level = 0.9
max_attempts = 2
retry_interval = 1

# Replace 'path/to/your/image.png' with the path to your image file
image_paths = [
    'Assets/UseItem.PNG',
    'Assets/Confirm.PNG',
    'Assets/Retry.png',
    'Assets/MySupp.png',
    'Assets/GoToQuest.png',
    'Assets/StartBattle.PNG',
]

def check_current_state( confidence, retry_interval):
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    for path in image_paths:
        try:
            tools.check_for_f1()
            
            template = cv2.imread(path)
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                return max_loc
            else:
                screenshot=None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1
        except Exception as e:
            print(f"Error while processing image for path {path}: {e}")
        
        time.sleep(retry_interval)

    #print("Exceeded max attempts for all images. No image found.")
    return None



def find_image_on_screen(image_paths, confidence, retry_interval):
    for path in image_paths:
        try:
            tools.check_for_f1()
            screenshot = pyautogui.screenshot()
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            template = cv2.imread(path)
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                return max_loc
            else:
                screenshot=None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1
        except Exception as e:
            print(f"Error while processing image for path {path}: {e}")
        
        time.sleep(retry_interval)

    #print("Exceeded max attempts for all images. No image found.")
    return None


def find_and_click(image_paths, confidence, max_attempts, retry_interval):
    while max_attempts > 0:  # Run continuously

        location = find_image_on_screen(image_paths, confidence, retry_interval)


        if location is not None:
            # Use the size of the template image found on screen
            template_width = cv2.imread(image_paths[0]).shape[1]
            template_height = cv2.imread(image_paths[0]).shape[0]
            
            center_x = location[0] + template_width // 2
            center_y = location[1] + template_height // 2
            pyautogui.click(center_x, center_y)
        else:
            if max_attempts > 1:
                location = None
                #print("No image found, attempting again...")
                #max_attempts = max_attempts - 1
            else:
                print("No image found after max attempts. Stopping.")

                # Capture and save screenshot
                capture_and_save_screenshot()
                max_attempts = 0

                break  # Stop the loop if no image is found after max attempts

        time.sleep(1)


if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    # Instance
    # relatorio_erro = log.MemoryLogger()
    # sys.stdout = relatorio_erro

    # Call the function with the specified image path and confidence level
    find_and_click(image_paths, confidence_level, max_attempts, retry_interval)

    # Restore sys.stdout to the original state
    # sys.stdout = sys.__stdout__
