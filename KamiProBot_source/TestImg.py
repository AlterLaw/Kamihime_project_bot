import cv2
import numpy as np
import pyautogui
import Libraries.img_arraysV3 as imgV3


def image_exists(folder_path):
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(folder_path)
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)


enemy_int = 0
array_value = "supp_request"

array = imgV3.screen_elements()
enemy = imgV3.raid_boss_list()
print(enemy[enemy_int])
image_exists(enemy[enemy_int])

print(array[array_value])
image_exists(array[array_value])
