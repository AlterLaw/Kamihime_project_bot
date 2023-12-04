import psutil
import pyautogui
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgV3


def searchingBattle(tela, params):
    expected = [
        params["elements"]["daily_raid_begin"],
        params["elements"]["daily_raid_begin"],
    ]


def battleFound():
    expected = [
        params["elements"]["raid_quests"],
        params["elements"]["challenge"],
        params["elements"]["item"],
        params["elements"]["confirm"],
        params["elements"]["my_supp"],
        params["elements"]["to_quest"],
    ]


def in_battle():
    expected = [
        params["elements"]["supp_req"],
        params["elements"]["item"],
        params["elements"]["start_battle"],
    ]


def current_state_verification(tela, params):
    caminho = params["V3"].verification_elements()
    selected_location, selected_path = iterate_over_array(caminho, params, tela)

    expected = [
        params["elements"]["raid_quests"],
        params["elements"]["supp_req"],
        params["elements"]["battle_won"],
    ]
    location, path = iterate_over_array(expected, params, tela)

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
    tela = capture_screenshot()

    params["state"] = current_state_verification(tela, params)

    if params["state"] == "raid_list":
        searchingBattle(tela, params)

    print()


if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    try:
        current_process = psutil.Process()
        lowest_record = current_process.memory_info()
        highest_record = current_process.memory_info()
        print("Process loaded")

        instance = imgsV3
        print("Image paths loaded")

    except Exception as e:
        print(f"Error loading a library. Error: {e}")

    running = True  # 1
    loop_counter = 1  # 2
    quests_counter = 0  # 3
    state = "Danone"  # 4
    confidence_level = 0.9  # 5
    screen_elements = instance.screen_elements()

    params = {
        "prc": current_process,
        "prc_low": lowest_record,
        "prc_high": highest_record,
        "run": running,
        "Lcount": loop_counter,
        "Qcount": quests_counter,
        "state": state,
        "elements": screen_elements,
        "V3": instance,
        "conf": confidence_level,
        "scr": pyautogui,
    }

    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")

    while params["run"]:
        update(params)
