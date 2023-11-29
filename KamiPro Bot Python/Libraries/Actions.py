import cv2


def my_supp(screenshot_np,confidence):
    path = 'Assets/MySupp.png'
    template = cv2.imread(path)
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
    if max_val >= confidence:
        return max_loc, path
    else:
        return None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1s

def go_to_quest(screenshot_np,confidence):
    path = 'Assets/GoToQuest.png'
    template = cv2.imread(path)
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
    if max_val >= confidence:
        return max_loc, path
    else:
        return None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1s