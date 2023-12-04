import cv2
import numpy as np
import pyautogui
import Libraries.img_arraysV3 as imgV3


def count_images_on_screen(template, threshold=0.9):
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)

    if len(locations) == 2:  # Check if locations has two dimensions
        count = 0
        
    else:
        count = 0

    return locations


def image_exists(template, name):
    count = count_images_on_screen(template)
    print(f"A imagem {name} apareceu {count} vezes na tela.")


enemy_int = 31
array_value = "daily_raid_begin"

array = imgV3.screen_elements()
enemy = imgV3.raid_boss_list()

print(enemy[enemy_int])
template_enemy = cv2.imread(enemy[enemy_int])
image_exists(template_enemy, f"Raid Boss {enemy_int}")

#print(array[array_value])
#template_array = cv2.imread(array[array_value])
#image_exists(template_array, array_value)
