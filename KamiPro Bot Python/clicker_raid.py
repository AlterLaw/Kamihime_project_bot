import psutil
from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import Libraries.img_arrays as imgs
import numpy as np
import pyautogui
import time
import sys
import cv2

def iterate_over_single(path,params):
    confidence,in_combat =params  
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
  
    try:
        tools.check_for_f1()
            
        template = cv2.imread(path)
        result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
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
        


    #print("Exceeded max attempts for all images. No image found.")
    return None, None

    
def iterate_over_array(image_paths, params):
    confidence,in_combat=params
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    for path in image_paths:
        try:
            tools.check_for_f1()
            template = cv2.imread(path)
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                return max_loc, path
            else:
                screenshot=None
                #print(f"Image not found for path: {path}. Skipping to the next image.")
                #sucess_counter=sucess_counter+1
        except Exception as e:
            print("Error on iteration over array")
            print(f"Error while processing image for path {path}: {e}")
        
        

    #print("Exceeded max attempts for all images. No image found.")
    return None, None


def collect_rewards(params,state):
    
    collecting = True
    while collecting:
        multi_path=imgs.reward_collecting()
        selected_location, selected_path= iterate_over_array(multi_path,params)
        print(selected_path)
        if selected_path=='Assets\_return_to_raids.PNG':
            collecting=False
            
        clicker(selected_location,selected_path)

    state="raid_battle_list"
    return state
        
def detect_reward():
    multi_path=imgs.reward_collecting()
    selected_location, selected_path= iterate_over_array(multi_path,params)
    if selected_location is not None and selected_path is not multi_path[2]:
        print("Oh look! a reward!")
        return True
    else:
        return False
def refresh(params):
    single_path="Assets\_raid_events.PNG"
    location, path= iterate_over_single(single_path,params)
    if location is not None:    
        clicker(location,path)
    single_path="Assets\_regular_raids.PNG"
    location, path= iterate_over_single(single_path,params)
    if location is not None:    
        clicker(location,path)


def look_for_raids(state,params):

    multi_path=imgs.raid_boss_priority()
    selected_location, selected_path= iterate_over_array(multi_path,params)

    print(selected_path)
    if selected_path == multi_path[0]:
        print("No Raids, refreshing...")
        refresh(params)
            
    elif selected_location != None and selected_path is not 'Assets\_no_battles.PNG':


        if detect_reward():
            collect_rewards(params)
            return state
        else:

            state = "pre_battle"
            print(f"State changed to {state}")
            clicker(selected_location,selected_path)

        return state
    else:
        refresh(params)
        return state 
    


    return state
        

def use_item(params):

    
    single_path="Assets\_use_item.PNG"
    location, path= iterate_over_single(single_path,params)

    if location is not None:
        clicker(location,path)
        
        single_path= "Assets\_confirm.PNG"
        location, path= iterate_over_single(single_path,params)
            
        clicker(location,path)


def pre_battle(params,state):

    multi_path=imgs.pre_battle_array()
    selected_location, selected_path= iterate_over_array(multi_path,params)

    print(selected_path)


    if selected_location is not None:
        clicker(selected_location,selected_path)

        if selected_path is multi_path[2]:
            if detect_reward():
                collect_rewards(params,state)

            selected_location, selected_path= iterate_over_array(multi_path,params)
            print("Checando se há confirmação de batalha")
            print(selected_path)
            if selected_path is multi_path[1]:
                print("Battle has been finished...")
                state = "raid_battle_list"
                clicker(selected_location,selected_path)
                print(f"State changed to {state}")
            else:
                clicker(selected_location,selected_path)
                state = "in_battle"
                print(f"State changed to {state}")
                return state


    
    return state
    


def in_battle(params,state):
    confidence,in_combat = params

    if in_combat:
        print("Fighting...")
        multi_path=imgs.check_if_battle_ended()
        selected_location, selected_path= iterate_over_array(multi_path,params)
        
        if selected_location is not None:
            print(selected_path)
            clicker(selected_location,selected_path)
            in_combat=False
            params = [confidence,in_combat]
            state = "end_battle"
            print("Ending combat")
        else:
            time.sleep(5)
            
    else:
        multi_path=imgs.in_battle_array()
        selected_location, selected_path= iterate_over_array(multi_path,params)
        if selected_location is not None:
            clicker(selected_location,selected_path)

        if selected_path == 'Assets\_start_battle.PNG':
            clicker(selected_location,selected_path)
            in_combat = True
            params = [confidence,in_combat]
            print("NCombat enabled")
    
        
    print("Battle function ended")
    return params, state 

def battle_finished(params,state):

    print("Fight ended")
    multi_path=imgs.battle_ending()
    selected_location, selected_path= iterate_over_array(multi_path,params)
    print(selected_path)
    if selected_location is not None:
        clicker(selected_location,selected_path)
        if selected_path ==multi_path[2]:
            state = "raid_battle_list"
            time.sleep(1)
            
    single_path="Assets\_raid_boss_available.PNG"
    location, path=iterate_over_single(single_path,params)
    clicker(location,path)
    print("Battle finished function ended")
    return state
    

        

def clicker(location,path):
    if location is not None:
        # Use the size of the template image found on screen
        template_width = cv2.imread(path).shape[1]
        template_height = cv2.imread(path).shape[0]
            
        center_x = location[0] + template_width // 2
        center_y = location[1] + template_height // 2
        pyautogui.click(center_x, center_y)
        time.sleep(2)


def debug(params):
    single_path='Assets\_raid_reward.PNG'
    location, path= iterate_over_single(single_path,params)

    multi_path=imgs.raid_boss_priority()
    selected_location, selected_path= iterate_over_array(multi_path,params)

    print(selected_location)
    print(selected_path)



def stats_screen(state,loop,process,quests):
    print("---------------------")
    print("KamiPro bot running")
    print("---------------------")
    print("Hold F1 to cancel execution")
    print(f"Current update loop: {loop}")
    print(f"Quests completed: {quests}")
    
    print(f"Current state: {state}")
    memory_info = process.memory_info()
    print(f"Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")



def update(params):
    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")
    current_process = psutil.Process()
    state= "raid_battle_list"
    update_loop_counter= 1
    quests_completed_counter=0
    running=True

    while running:

        if state == "raid_battle_list":
            print(f"Current state: {state}")
            if detect_reward():
                state = collect_rewards(params,state)

            state = look_for_raids(state,params)
            use_item(params)

            
        if state == "pre_battle":
            print(f"Current state: {state}")
            if detect_reward():
                state = collect_rewards(params,state)
            state = pre_battle(params,state)

        if state == "in_battle":
            print(f"Current state: {state}")
            params,state=in_battle(params,state)
        if state == "end_battle":
            print(f"Current state: {state}")
            state = battle_finished(params,state)
            if state is "raid_battle_list":
                quests_completed_counter+=1



        time.sleep(1)
        tools.check_for_f1()
        tools.clear_console()
        stats_screen(state,update_loop_counter,current_process,quests_completed_counter)
        update_loop_counter+=1
        





if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    confidence_level = 0.85
    in_combat =False

    params = [confidence_level,in_combat]

    update(params)
    
    #debug(params)
    #single_path='Assets\_confirm.PNG'
    #location, path= iterate_over_single(single_path,params)
    #print(location, path)



