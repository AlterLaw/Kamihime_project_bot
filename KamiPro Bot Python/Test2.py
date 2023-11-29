import os
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


array=imgV3.screen_elements()

\
print(array["select_raid"])
image_exists(array["notice"])