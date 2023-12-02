
import cv2
import numpy as np
import psutil
import pyautogui
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgV3


def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_np

def iterate_over_single(path,params,tela):
         
    try:
        tools.check_for_f1()
            
        template = cv2.imread(path)
        result = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= params["conf"]:
            return max_loc, path
        else:
            screenshot=None
            #print(f"Image not found for path: {path}. Skipping to the next image.")
            #sucess_counter=sucess_counter+1
    except Exception as e:
        print("Error on iteration over single")
        print(f"Error while processing image for path {path}: {e}")
        
    return None, None

def iterate_over_array(image_paths, params,tela):



    for path in image_paths:
        try:
            tools.check_for_f1()
            template = cv2.imread(path)
            result = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= params["conf"]:
                return max_loc, path
            else:
                screenshot=None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1
        except Exception as e:
            print("Error on iteration over array")
            print(f"Error while processing image for path {path}: {e}")
        
    return None, None


def searchingBattle(tela,params):

    expected=[
        params["elements"]["daily_raid_begin"],
        params["elements"]["daily_raid_begin"],
    ]
    


def battleFound():

    expected=[
        params["elements"]["raid_quests"],
        params["elements"]["challenge"],
        params["elements"]["item"],
        params["elements"]["confirm"],
        params["elements"]["my_supp"],
        params["elements"]["to_quest"], 
        
    ]

def in_battle():

        expected=[
        params["elements"]["supp_req"],
        params["elements"]["item"],
        params["elements"]["start_battle"], 
    ]


def current_state_verification(tela,params):
    
    caminho=params["V3"].verification_elements()
    selected_location, selected_path= iterate_over_array(caminho,params,tela)
    
    expected=[
        params["elements"]["raid_quests"],
        params["elements"]["supp_req"],
        params["elements"]["battle_won"], 
    ]
    location,path=iterate_over_array(expected,params,tela)


    if selected_path == params["elements"]["raid_quests"]:
        params["state"] = "raid_list"
        return params

    if selected_path == params["elements"]["supp_req"]:
        params["state"] = "battle_found"
        return params

    if selected_path == params["elements"]["mid_battle"]:
        params["state"] = "fight_on"
        return params
    
    if selected_path == params["elements"]["battle_won"]:
        params["state"] = "fight_won"
        return params
    
    if selected_path == None:

        return params


def update(params):
    tela= capture_screenshot()
    
    params["state"]= current_state_verification(tela,params)

    if params["state"] == "raid_list":
        searchingBattle(tela,params)


    print()


if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    current_process = psutil.Process() #0
    if current_process is not None:
        print("Process loaded")
    
    instance=imgV3
    if instance is not None:
        print("Image paths loaded")   

    screen_elements= instance.screen_elements()
    if screen_elements is not None:
        print("Screen elements paths loaded")   

    running=True #1
    loop_counter= 1 #2
    quests_counter=0 #3
    state= "Danone" #4
    confidence_level = 0.85 #5

    params = {
    "prc": current_process,
    "V3": instance,
    "elements":screen_elements,
    "run": running,
    "Lcount": loop_counter,
    "Qcount": quests_counter,
    "state": state,
    "conf": confidence_level,
    "scr": pyautogui
}


    update(params)