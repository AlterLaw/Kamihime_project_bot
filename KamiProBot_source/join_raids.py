import traceback
import psutil
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgsV3
import numpy as np
import pyautogui
import time


def refresh(params):
    src = tools.capture_screenshot()
    single_path = params["elements"]["r_events"]
    location, path = tools.search_single_on_single(single_path, params["conf"], src)

    if location is not None:
        tools.clicker(location, path)

    src = tools.capture_screenshot()
    single_path = params["elements"]["r_regular"]
    location, path = tools.search_single_on_single(single_path, params["conf"], src)
    if location is not None:
        tools.clicker(location, path)


def current_state_verification(tela, params):

    possibilities=[
        params["elements"]["select_raid"],
        params["elements"]["select_supp"],
        params["elements"]["supp_request"],
        params["elements"]["battle_lost"],
        params["elements"]["battle_gu"],
        params["elements"]["mid_battle"],
        params["elements"]["battle_won"],
        params["elements"]["popup"],
    ]

    selected_location, selected_path = tools.search_single_on_array(
        possibilities, params["conf"], tela
    )
    print(f"CurrentState: {params["state"]}")
    if selected_path == params["elements"]["select_raid"]:
        params["state"] = "raid_list"
        return params

    if selected_path == params["elements"]["select_supp"]:
        params["state"] = "pre_fight"
        return params

    if selected_path == params["elements"]["supp_request"]:
        params["state"] = "fight_off"
        return params

    if selected_path == params["elements"]["mid_battle"]:
        params["state"] = "fight_on"
        return params

    if (selected_path == params["elements"]["popup"]
        or selected_path == params["elements"]["boss_available"]):
        params["state"] = "main_menu"
        print(params["state"])
        return params

    if (selected_path == params["elements"]["battle_lost"]
        or selected_path == params["elements"]["battle_gu"]):
        params["state"] = "fight_lost"
        return params

    if selected_path == params["elements"]["battle_won"]:
        params["state"] = "fight_won"
        return params

    if selected_path == None:
        return params


def look_for_raids(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    location, path = tools.search_single_on_single(
        objects["r_reward"], params["conf"], tela
    )

    if path is not None:
        tools.clicker(location, path)
        tela = tools.capture_screenshot()

        location, path = tools.search_single_on_single(
            objects["r_sucess"], params["conf"], tela
        )
        tools.clicker(location, path)
        return

    location, path = tools.search_single_on_single(
        objects["No_btt"], params["conf"], tela
    )

    if path is not None:
        refresh(params)
        return params

    selected_location, selected_path = tools.search_single_on_array(
        params["V3"].raid_boss_list(), params["conf"], tela
    )

    if selected_path is not None:
        tools.clicker(selected_location, selected_path)
        return params

    else:
        tela = tools.capture_screenshot()
        location, path = tools.search_single_on_single(
            objects["item"], params["conf"], tela
        )

        if path is not None:
            tools.clicker(location, path)
            tela = tools.capture_screenshot()
            location, path = tools.search_single_on_single(
                objects["confirm"], params["conf"], tela
            )

            tools.clicker(location, path)
        else:
            refresh(params)
            return params

    return params


def pre_battle(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    location, path = tools.search_single_on_single(
        objects["my_supp"], params["conf"], tela
    )

    if path is not None:
        tools.clicker(location, path)

    location, path = tools.search_single_on_single(
        objects["go_to_quest"], params["conf"], tela
    )

    if path is not None:
        tools.clicker(location, path)

    possibilities = [
        objects["confirm"],
        objects["r_sucess"],
        objects["return_to_raids"],
    ]
    tela = tools.capture_screenshot()
    location, path = tools.search_single_on_array(possibilities, params["conf"], tela)

    if path is not None:
        tools.clicker(location, path)
        tela = tools.capture_screenshot()
        location, path = tools.search_single_on_array(
            possibilities, params["conf"], tela
        )

        if path is params["elements"]["confirm"]:
            params["state"] = "raid_list"
            tools.clicker(location, path)
            return params

        if path is params["elements"]["r_sucess"]:
            tools.clicker(location, path)

        if path is params["elements"]["return_to_raids"]:
            params["state"] = "raid_list"
            tools.clicker(location, path)
            return params

    return params


def offbattle(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    location, path = tools.search_single_on_single(
        objects["supp_request"], params["conf"], tela
    )

    if path is not None:
        tools.clicker(location, path)

    return params


def onbattle(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()
    location, path = tools.search_single_on_single(
        objects["start_battle"], params["conf"], tela
    )

    if path is not None:
        tools.clicker(location, path)
        return params
    else:
        time.sleep(5)
        return params


def victory(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    possibilities = [
        objects["confirm"],
        objects["return_to_raids"],
    ]
    location, path = tools.search_single_on_array(possibilities, params["conf"], tela)

    print(path)
    if path is not None:
        tools.clicker(location, path)
        if path is objects["return_to_raids"]:
            params["Qcount"] += 1
    return params


def loss(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    possibilities = [
        objects["go_to_my_page"],
        objects["cancel"],
        objects["boss_available"],
    ]
    location, path = tools.search_single_on_array(possibilities, params["conf"], tela)
    print(f"Path: {path}")

    if path is not None:
        tools.clicker(location, path)
    return params


def menu(params):
    tela = tools.capture_screenshot()
    objects = params["V3"].screen_elements()

    possibilities = [
        objects["popup"],
        objects["boss_available"],
    ]
    location, path = tools.search_single_on_array(possibilities, params["conf"], tela)

    if path is not None:
        tools.clicker(location, path)
        return params
    return params


def update(params):
    """
    params["prc"]
    params["run"]
    params["Lcount"]
    params["Qcount"]
    params["state"]
    params["conf"]
    params["in_fgt"]
    """

    tela_atual = tools.capture_screenshot()
    params = current_state_verification(tela_atual, params)

    if params["state"] == "raid_list":
        try:
            params = look_for_raids(params)
            print("Choose raid")
        except Exception as e:
            print(f"Erro: {e}")
        traceback.print_exc()

    if params["state"] == "main_menu":
        try:
            params = menu(params)
            print("menu")
        except Exception as e:
            print(f"Erro: {e}")
            traceback.print_exc()

    if params["state"] == "pre_fight":
        try:
            params = pre_battle(params)
            print("Preparing to fight")
        except Exception as e:
            print(f"Erro: {e}")
            traceback.print_exc()

    if params["state"] == "fight_off":
        try:
            params = offbattle(params)
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
            params = victory(params)
            print("Victory!")
        except Exception as e:
            print(f"Erro: {e}")
            traceback.print_exc()

    if params["state"] == "fight_lost":
        try:
            params = loss(params)
            print("Lost...")
        except Exception as e:
            print(f"Erro: {e}")
            traceback.print_exc()

    tools.check_for_f1()
    #tools.clear_console()
    params["prc_high"], params["prc_low"] = tools.stats_screen(
        params["prc"],
        params["prc_high"],
        params["prc_low"],
        params["Qcount"],
        params["state"],
    )
    params["Lcount"] += 1


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
