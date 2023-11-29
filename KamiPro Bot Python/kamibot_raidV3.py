import traceback
import psutil
from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgsV3
import numpy as np
import pyautogui
import time
import sys
import cv2


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

def refresh(params):

    src=capture_screenshot()
    single_path=params["elements"]["r_events"]
    location, path= iterate_over_single(single_path,params,src)

    if location is not None:    
        clicker(location,path)

    src=capture_screenshot()
    single_path=params["elements"]["r_regular"]
    location, path= iterate_over_single(single_path,params,src)
    if location is not None:    
        clicker(location,path)


def clicker(location,path):
    if location is not None:
        # Use the size of the template image found on screen
        template_width = cv2.imread(path).shape[1]
        template_height = cv2.imread(path).shape[0]
            
        center_x = location[0] + template_width // 2
        center_y = location[1] + template_height // 2
        pyautogui.click(center_x, center_y)
        time.sleep(3)


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

def current_state_verification(tela,params):
    
    caminho=params["V3"].verification_elements()
    selected_location, selected_path= iterate_over_array(caminho,params,tela)
    print(params["state"])
    if selected_path == params["elements"]["select_raid"]:
        params["state"] = "raid_list"
        return params

    if selected_path == params["elements"]["select_supp"]:
        params["state"] = "pre_fight"
        return params
    
    if selected_path == params["elements"]["request_support"]:
        params["state"] = "fight_off"
        return params

    if selected_path == params["elements"]["mid_battle"]:
        params["state"] = "fight_on"
        return params
    
    if selected_path == params["elements"]["popup"] or selected_path == params["elements"]["boss_available"] :
        params["state"] = "main_menu"
        print(params["state"])
        return params

    if selected_path == params["elements"]["battle_lost"] or selected_path == params["elements"]["battle_gu"]:
        params["state"] = "fight_lost"
        return params
    
    if selected_path == params["elements"]["battle_won"]:
        params["state"] = "fight_won"
        return params
    
    if selected_path == None:

        return params




def look_for_raids(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()

    location, path= iterate_over_single(objects["r_reward"],params,tela)

    if path is not None:
        clicker(location,path)
        tela=capture_screenshot()
        object1=objects["r_sucess"]
        location, path= iterate_over_single(object1,params,tela)
        clicker(location,path)
        return

    location, path= iterate_over_single(objects["No_btt"],params,tela)
    
    if path is not None:
        refresh(params)
        return params

    selected_location, selected_path= iterate_over_array(params["V3"].raid_boss_list(),params,tela)

    if selected_path is not None:
            clicker(selected_location,selected_path)
            return params
        
    else:
        tela=capture_screenshot()
        location, path= iterate_over_single(objects["item"],params,tela)

        if path is not None:
            clicker(location,path)
            tela=capture_screenshot()
            location, path= iterate_over_single(objects["confirm"],params,tela)
            clicker(location,path)
        else:
            refresh(params)
            return params
        
    return params


def pre_battle(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()

    location, path= iterate_over_single(objects["my_supp"],params,tela)

    if path is not None:
        clicker(location,path)
        
    location, path= iterate_over_single(objects["to_quest"],params,tela)

    if path is not None:
        clicker(location,path)


    possibilities=[
            objects["confirm"],
            objects["r_sucess"],
            objects["return_to_raids"],
            ]
    tela=capture_screenshot()
    location, path= iterate_over_array(possibilities,params,tela)

    if path is not None:
        clicker(location,path)
        tela=capture_screenshot()
        location, path= iterate_over_array(possibilities,params,tela)
        if path is params["elements"]["confirm"]:
            params["state"]= "raid_list"
            clicker(location,path)
            return params

        if path is params["elements"]["r_sucess"]:
            clicker(location,path)

        if path is params["elements"]["return_to_raids"]: 
            params["state"]= "raid_list"
            clicker(location,path)
            return params
    
    
    return params

def offbattle(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()

    location, path= iterate_over_single(objects["supp_req"],params,tela)

    if path is not None:
        clicker(location,path)



    return params
        

def onbattle(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()
    location, path= iterate_over_single(objects["start_battle"],params,tela)

    if path is not None:
        clicker(location,path)
        return params
    else:
        
        time.sleep(5)
        return params

def victory(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()

    possibilities=[
            objects["confirm"],
            objects["return_to_raids"],
            ]
    location, path= iterate_over_array(possibilities,params,tela)
    print(path)
    if path is not None:
        clicker(location,path)
        if path is objects["return_to_raids"]:
            params["Qcount"]+=1
    return params

def loss(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()

    possibilities=[
            objects["return_to_raids"],
            objects["cancel"],
            ]
    location, path= iterate_over_array(possibilities,params,tela)

    if path is not None:
        clicker(location,path)
    return params


def menu(params):
    tela=capture_screenshot()
    objects=params["V3"].screen_elements()
    

    possibilities=[
            objects["popup"],
            objects["boss_available"],
            ]
    location, path= iterate_over_array(possibilities,params,tela)

    if path is not None:
        clicker(location,path)
        return params
    return params
    
    




        


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
        tela_atual = capture_screenshot()

        params=current_state_verification(tela_atual,params)

        print(params["state"])


        if params["state"] == "raid_list":
            try:
                params=look_for_raids(params)
                print("Choose raid") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()

        if params["state"] == "main_menu":
            try:
                params=menu(params)
                print("menu") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()

        if params["state"] == "pre_fight":
            try:
                params=pre_battle(params)
                print("Preparing to fight") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()

        if params["state"] == "fight_off":
            try:
                params=offbattle(params)
                print("Request supp?") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc() 

        if params["state"] == "fight_on":
            try:
                params = onbattle(params)
                print("Fighting...") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()

        if params["state"] == "fight_won":
            
            try:
                params=victory(params)
                print("Victory!") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()

        if params["state"] == "fight_lost":
            try:
                params=loss(params)
                print("Lost...") 
            except Exception as e:
                print(f"Erro: {e}")
                traceback.print_exc()


        tools.check_for_f1()
        tools.clear_console()
        stats_screen(params)
        params["Lcount"]+=1
        

if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    current_process = psutil.Process() #0
    if current_process is not None:
        print("Process loaded")
    instance=imgsV3
    if instance is not None:
        print("Image paths loaded")    
    running=True #1
    loop_counter= 1 #2
    quests_counter=0 #3
    state= "Danone" #4
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
    "V3": instance,
    "scr": pyautogui

}


    update(params)
    
    #debug(params)
    #single_path='Assets\_confirm.PNG'
    #location, path= iterate_over_single(single_path,params)
    #print(location, path)



