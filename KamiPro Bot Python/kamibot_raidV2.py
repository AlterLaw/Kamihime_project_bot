import psutil
from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import Libraries.img_arraysV2 as imgsV2
import numpy as np
import pyautogui
import time
import sys
import cv2

def iterate_over_single(path,params):
     
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    try:
        tools.check_for_f1()
            
        template = cv2.imread(path)
        result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
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

    
def iterate_over_array(image_paths, params):

    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    time.sleep(1)

    for path in image_paths:
        try:
            tools.check_for_f1()
            template = cv2.imread(path)
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
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


def collect_rewards(params):
    
    collecting = True
    
    while collecting:
        
        multi_path=params["V2"].expected_buttons_rewards()
        if multi_path is None:
            multi_path= imgsV2.expected_buttons_rewards()
            params["V2"]=imgsV2

        selected_location, selected_path= iterate_over_array(multi_path,params)
        if selected_path is params["elements"]["return_to_raids"]:
            collecting=False
            
        clicker(selected_location,selected_path)

    params["state"]="raid_battle_list"
    return params
        

def verification(params):
    location, path= iterate_over_single(params["elements"]["confirm"],params)

    if path is not None:
        return location,path
    else:
        return None, None

def detect_reward(params):
    multi_path=params["V2"].scan_for_rewards()

    if multi_path is None:
        multi_path= imgsV2.raid_boss_priority()
        params["V2"]=imgsV2
    
    selected_location, selected_path= iterate_over_array(multi_path,params)
    
    if selected_location is not None:
        print("Oh look! a reward!")
        return True
    else:
        return False
    


def refresh(params):
    
    single_path=params["elements"]["r_events"]
    location, path= iterate_over_single(single_path,params)

    if location is not None:    
        clicker(location,path)

    single_path=params["elements"]["r_regular"]
    location, path= iterate_over_single(single_path,params)
    if location is not None:    
        clicker(location,path)


def look_for_raids(params):

    multi_path=params["V2"].raid_boss_priority()
    if multi_path is None:
        multi_path= imgsV2.raid_boss_priority()
        params["V2"]=imgsV2
        print("I remember what is imgs")

    selected_location, selected_path= iterate_over_array(multi_path,params)

    print(selected_path)
    if selected_path == multi_path[0]:
        print("No Raids, refreshing...")
        refresh(params)
            
    elif selected_path is not None:
        clicker(selected_location,selected_path)

        params["state"] = "pre_battle"
        print(f"State changed to {params["state"]}")


    else:
        refresh(params)
    
    return params
        

def use_item(params):

    single_path = params["elements"]["item"]
    print(single_path)

    location, path= iterate_over_single(single_path,params)
    print("Checking need for itens")

    if location is not None:
        clicker(location,path)

        print("Using itens...")    
        single_path= params["elements"]["confirm"]
        location, path= iterate_over_single(single_path,params)
        clicker(location,path)



def pre_battle(params):

    multi_path=params["V2"].expected_buttons_pre_battle()
    if multi_path is None:
        multi_path= imgsV2.expected_buttons_pre_battle()
        params["V2"]=imgsV2
    selected_location, selected_path= iterate_over_array(multi_path,params)
    print(f"Pre battle path is: {selected_path}")

    if selected_path is params["elements"]["my_supp"]:
        print("MySupp")
        clicker(selected_location,selected_path)

        return params

    if selected_path is params["elements"]["to_quest"]:
        print("To Quest")
        clicker(selected_location,selected_path)

        loc,pat=verification(params)
        if loc is not None:
            print("Battle has been finished...")
            clicker(loc,pat)
            params["state"] = "raid_battle_list"
            print(f"State changed to {params["state"]}")
        else:

            params["state"] = "battle_start"
            print(f"State changed to {params["state"]}")

        return params
    
    return params
    
def battle_start(params):
    multi_path=params["V2"].expected_buttons_in_battle()
    if multi_path is None:
        multi_path= imgsV2.expected_buttons_in_battle()
        params["V2"]=imgsV2
    selected_location, selected_path= iterate_over_array(multi_path,params)
    print()

    if selected_path is params["elements"]["supp_req"]:
        clicker(selected_location,selected_path)

    if selected_path is params["elements"]["start_battle"]:
        clicker(selected_location,selected_path)

        print("Combat enabled")
        params["state"] = "in_battle"

    return params

def in_battle(params):

    print("Fighting...")
    multi_path=params["V2"].checking_ending()
    if multi_path is None:
        multi_path= imgsV2.checking_ending()
        params["V2"]=imgsV2
    selected_location, selected_path= iterate_over_array(multi_path,params)

    if selected_path is params["elements"]["cancel"]:
        print("defeated...")
        clicker(selected_location,selected_path)
        params["state"] = "end_battle"
        print("Ending combat")
        return params
    else:

        if selected_path is params["elements"]["confirm"]:
            clicker(selected_location,selected_path)
            print("Victory!")
            params["state"] = "end_battle"
            print("Ending combat")
            return params
        
    
    return params

def battle_finished(params):

    print("Fight ended")
    multi_path= params["V2"].expected_buttons_in_ending()
    if multi_path is None:
        multi_path= imgsV2.expected_buttons_in_ending()
        params["V2"]=imgsV2
    selected_location, selected_path= iterate_over_array(multi_path,params)
    

    if selected_path is (params["elements"]["cancel"]):
        clicker(selected_location,selected_path)


    if selected_path is (params["elements"]["confirm"]):
        clicker(selected_location,selected_path)

  
    if selected_path is params["elements"]["go_to_my_page"]:
        print("Battle lost...")
        clicker(selected_location,selected_path)  

    if selected_path is params["elements"]["boss_available"]:
        params["state"] = "raid_battle_list"        
        clicker(selected_location,selected_path)  

    if selected_path is params["elements"]["return_to_raids"]:
        print("Battle won!")
        params["state"] = "raid_battle_list"
        clicker(selected_location,selected_path)


    return params
    

def clicker(location,path):
    if location is not None:
        # Use the size of the template image found on screen
        template_width = cv2.imread(path).shape[1]
        template_height = cv2.imread(path).shape[0]
            
        center_x = location[0] + template_width // 2
        center_y = location[1] + template_height // 2
        pyautogui.click(center_x, center_y)
        time.sleep(2)






def stats_screen(params):
    print("---------------------")
    print("KamiPro bot running")
    print("---------------------")
    print("Hold F1 to cancel execution")
    print(f"Current update loop: {params["Lcount"]}")
    print(f"Quests completed: {params["Qcount"]}")
    
    print(f"Current state: {params["state"]}")
    memory_info = params["prc"].memory_info()
    print(f"Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")



def update(params):
    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")
    
    """
    params["prc"]
    params["run"]
    params["Lcount"]
    params["Qcount"]
    params["state"]
    params["conf"]
    params["in_fgt"]
    """

    while params["run"]:


            
        if params["state"] is "raid_battle_list" or params["state"] is "pre_battle":
            if detect_reward(params):
                params = collect_rewards(params)

        if params["state"] == "raid_battle_list":
            print(f"Current state: {params["state"]}")
            params = look_for_raids(params)
            try:
                use_item(params)
            except Exception as e:
                print(f"Error while using item: {e}")
                print(f"Status:")
                print(f"Params is: {params}")
            
        
        if params["state"] == "pre_battle":
            print(f"Current state: {params["state"]}")
            params = pre_battle(params)
            try:
                use_item(params)
            except Exception as e:
                print(f"Error while using item: {e}")
                print(f"Status:")
                print(f"Params is: {params}")
        
        if params["state"] == "battle_start":
            print(f"Current state: {params["state"]}")
            params = battle_start(params)

        if params["state"] == "in_battle":
            print(f"Current state: {params["state"]}")
            params=in_battle(params)

        if params["state"] == "end_battle":
            print(f"Current state: {params["state"]}")
            params = battle_finished(params)
            if params["state"] is "raid_battle_list":
                params["Qcount"]+=1



        time.sleep(1)
        tools.check_for_f1()
        #tools.clear_console()
        stats_screen(params)
        params["Lcount"]+=1
        





if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    current_process = psutil.Process() #0
    if current_process is not None:
        print("Process loaded")
    instance=imgsV2
    if instance is not None:
        print("Image paths loaded")    
    running=True #1
    loop_counter= 1 #2
    quests_counter=0 #3
    state= "raid_battle_list" #4
    confidence_level = 0.85 #5
    screen_elements= instance.screen_elements()



    params = {
    "prc": current_process,
    "run": running,
    "Lcount": loop_counter,
    "Qcount": quests_counter,
    "state": state,
    "conf": confidence_level,
    "elements":screen_elements,
    "V2": instance,

}


    update(params)
    
    #debug(params)
    #single_path='Assets\_confirm.PNG'
    #location, path= iterate_over_single(single_path,params)
    #print(location, path)



