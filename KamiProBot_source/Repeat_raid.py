import psutil
from Libraries.Debug import capture_and_save_screenshot
import Libraries.LogRecorder as log
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgV3
import time
     
def battle_won(params):
    paths= params["L_paths"]
    iteration_list =[
        paths["challenge"],
        paths["confirm"],
        paths["item"],
        paths["retry"],
    ]

    location,path=tools.search_single_on_array(iteration_list,params["conf"],params["screen"])

    if path is not None:
        tools.clicker(location,path)

    if path is paths["retry"]:
        params["Qcount"]+=1
    return params

def in_battle(params):
    paths= params["L_paths"]
    iteration_list =[
        paths["supp_req"],
        paths["start_battle"],
        paths["burst"],
    ]
    location,path=tools.search_single_on_array(iteration_list,params["conf"],params["screen"])
    
    if path is not None and path is not paths["burst"]:
        tools.clicker(location,path)

    elif path is paths["burst"]:
        time.sleep(5)
    return params

def supp_selection(params):
    paths= params["L_paths"]
    iteration_list = [
        paths["my_supp"],
        paths["go_to_quest"],
        paths["item"],
        paths["confirm"],
            ]
    location,path=tools.search_single_on_array(iteration_list,params["conf"],params["screen"])
    if path is not None and path is not paths["burst"]:
        tools.clicker(location,path)
    return params


def detect_state(params):
    paths= params["L_paths"]
    iteration_list=[]
    expected_elements=[
        paths["select_supp"],
        paths["request_support"],
        paths["battle_won"]
    ]
    
    location,path=tools.search_single_on_array(expected_elements,params["conf"],params["screen"])

    if path== paths["select_supp"] :
        params["state"] = "pre_battle"
        
    if path== paths["request_support"]:
        params["state"] = "in_battle"
        
    if path== paths["battle_won"]:
        params["state"] = "battle_won"

    return params



def stats_screen(params):

    print("KamiPro bot running")
    print("---------------------")
    print("Hold F1 to cancel execution")
    print(f"Quests completed: {params["Qcount"]}")
    print(f"Current state: {params["state"]}")
    memory_info = params["prc"].memory_info()
    print(f"Used memory: {memory_info.rss / 1024 / 1024:.2f} MB")

    if memory_info> params["prc_high"]:
        params["prc_high"] = memory_info
    if memory_info <params["prc_low"]:
        params["prc_low"] = memory_info
    
    print(f"Lowest record: {params["prc_low"].rss / 1024 / 1024:.2f} MB")
    print(f"Highest record: {params["prc_high"].rss / 1024 / 1024:.2f} MB")


    #cpu_use = process.cpu_percent(interval=1)
    #print(f"Used CPU: {cpu_use}%")
    print("---------------------")
    return params

    

def update(params):
    
    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")

    while params["run"]:
        params["screen"]=tools.capture_screenshot()
        tools.clear_console()

        tools.check_for_f1()
        params=detect_state(params)
        params=stats_screen(params)

        if params["state"] is "pre_battle":
            params=supp_selection(params)

        if params["state"] is "in_battle":
            params=in_battle(params)
        if params["state"] is "battle_won":
            params=battle_won(params)

        if params["Qcount"]>60:
            params["run"]=False


        tools.check_for_f1()
        time.sleep(1)
        



if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    # Instance
    # relatorio_erro = log.MemoryLogger()
    # sys.stdout = relatorio_erro

    paths=imgV3.screen_elements()
    current_process = psutil.Process()
    lowest_record= current_process.memory_info()
    highest_record = current_process.memory_info()

    confidence_level = 0.9
    quests_completed_counter=0
    state="battle_off"
    running = True
    
    params = {
    "prc": current_process,
    "prc_low":lowest_record,
    "prc_high":highest_record,
    "run": running,
    "Qcount": quests_completed_counter,
    "state": state,
    "conf": confidence_level,
    "L_paths":paths,
    "screen": None
    }

    # Call the function with the specified image path and confidence level
    update(params)

    # Restore sys.stdout to the original state
    # sys.stdout = sys.__stdout__
