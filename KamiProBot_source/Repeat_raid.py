import psutil
import Libraries.Tools as tools
import Libraries.img_arraysV3 as imgV3
import time


def battle_lost(params):
    paths = params["L_paths"]
    iteration_list = [
        paths["cancel"],
        paths["confirm"],
        paths["mid_battle"],
    ]
    location, path = tools.search_single_on_array(
        iteration_list, params["conf"], params["screen"]
    )
    print(path)
    if path is not None and path is not paths["mid_battle"]:
        tools.clicker(location, path)

    elif path is paths["mid_battle"]:
        tools.clicker(location, path)
        time.sleep(5)

    return params


def battle_won(params):
    paths = params["L_paths"]
    iteration_list = [
        paths["challenge"],
        paths["confirm"],
        paths["item"],
        paths["retry"],
    ]

    location, path = tools.search_single_on_array(
        iteration_list, params["conf"], params["screen"]
    )

    if path is not None:
        tools.clicker(location, path)

    if path is paths["retry"]:
        params["Qcount"] += 1
    return params


def in_battle(params):
    paths = params["L_paths"]
    iteration_list = [
        paths["supp_req"],
        paths["start_battle"],
        paths["burst"],
    ]
    location, path = tools.search_single_on_array(
        iteration_list, params["conf"], params["screen"]
    )

    if path is not None and path is not paths["burst"]:
        tools.clicker(location, path)

    elif path is paths["burst"]:
        time.sleep(5)
    return params


def supp_selection(params):
    paths = params["L_paths"]
    iteration_list = [
        paths["my_supp"],
        paths["go_to_quest"],
        paths["item"],
        paths["confirm"],
    ]
    location, path = tools.search_single_on_array(
        iteration_list, params["conf"], params["screen"]
    )
    if path is not None and path is not paths["burst"]:
        tools.clicker(location, path)
    return params


def detect_state(params):
    paths = params["L_paths"]
    iteration_list = []
    expected_elements = [
        paths["select_supp"],
        paths["request_support"],
        paths["battle_lost"],
        paths["revive"],
        paths["battle_won"],
    ]

    location, path = tools.search_single_on_array(
        expected_elements, params["conf"], params["screen"]
    )

    if path == paths["select_supp"]:
        params["state"] = "pre_battle"

    if path == paths["request_support"]:
        params["state"] = "in_battle"

    if path == paths["battle_won"]:
        params["state"] = "battle_won"

    if path == paths["battle_lost"] or path == paths["revive"]:
        params["state"] = "battle_lost"

    return params


def update(params):
    print("KamiPro bot Initiating...")
    print("Hold F1 to cancel execution")

    while params["run"]:
        params["screen"] = tools.capture_screenshot()
        tools.clear_console()

        tools.check_for_f1()
        params = detect_state(params)
        params["prc_high"], params["prc_low"] = tools.stats_screen(
            params["prc"],
            params["prc_high"],
            params["prc_low"],
            params["Qcount"],
            params["state"],
        )

        if params["state"] is "pre_battle":
            params = supp_selection(params)

        if params["state"] is "in_battle":
            params = in_battle(params)
        if params["state"] is "battle_won":
            params = battle_won(params)

        if params["state"] is "battle_lost":
            params = battle_lost(params)

        if params["Qcount"] > 13:
            params["run"] = False

        tools.check_for_f1()
        time.sleep(1)


if __name__ == "__main__":
    # Clears the console
    tools.clear_console()

    paths = imgV3.screen_elements()
    current_process = psutil.Process()
    lowest_record = current_process.memory_info()
    highest_record = current_process.memory_info()

    confidence_level = 0.9
    quests_completed_counter = 0
    state = "battle_off"
    running = True

    params = {
        "prc": current_process,
        "prc_low": lowest_record,
        "prc_high": highest_record,
        "run": running,
        "Qcount": quests_completed_counter,
        "state": state,
        "conf": confidence_level,
        "L_paths": paths,
        "screen": None,
    }

    update(params)
