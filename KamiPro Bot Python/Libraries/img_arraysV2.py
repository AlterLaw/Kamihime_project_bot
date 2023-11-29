def raid_boss_priority():
    raid_boss_paths = [

    'Assets\_no_battles.PNG',
    'Assets\Raid_Boss\_phantom_T1.PNG',

    'Assets\Raid_Boss\_dark_T5.PNG',
    'Assets\Raid_Boss\_light_T5.PNG',
    'Assets\Raid_Boss\_wind_T5.PNG',
    'Assets\Raid_Boss\_thunder_T5.PNG',  
    'Assets\Raid_Boss\_water_T5.PNG',   
    'Assets\Raid_Boss\_fire_T5.PNG',
    
    'Assets\Raid_Boss\_dark_T4.PNG',
    'Assets\Raid_Boss\_light_T4.PNG',
    'Assets\Raid_Boss\_wind_T4.PNG',
    'Assets\Raid_Boss\_thunder_T4.PNG',  
    'Assets\Raid_Boss\_water_T4.PNG',    
    'Assets\Raid_Boss\_fire_T4.PNG',
    
    'Assets\Raid_Boss\_dark_T3.PNG',
    'Assets\Raid_Boss\_light_T3.PNG',
    'Assets\Raid_Boss\_wind_T3.PNG',
    'Assets\Raid_Boss\_thunder_T3.PNG',  
    'Assets\Raid_Boss\_water_T3.PNG',    
    'Assets\Raid_Boss\_fire_T3.PNG',

    'Assets\Raid_Boss\_dark_T2.PNG',
    #'Assets\Raid_Boss\_light_T2.PNG',
    'Assets\Raid_Boss\_wind_T2.PNG',
    'Assets\Raid_Boss\_thunder_T2.PNG',  
    #'Assets\Raid_Boss\_water_T2.PNG',
    #'Assets\Raid_Boss\_fire_T2.PNG',

    'Assets\Raid_Boss\_dark_T1.PNG',
    #'Assets\Raid_Boss\_light_T1.PNG',
    'Assets\Raid_Boss\_wind_T1.PNG',
    'Assets\Raid_Boss\_thunder_T1.PNG',  
    'Assets\Raid_Boss\_water_T1.PNG',   
    'Assets\Raid_Boss\_fire_T1.PNG',
    ]
    return raid_boss_paths

def screen_elements():

    elements = {
    "my_supp": 'Assets\_my_supp.png',
    "to_quest": 'Assets\_go_to_quest.png',
    "confirm": 'Assets\_confirm.PNG',
    "cancel": 'Assets\_cancel.PNG',
    "r_reward": 'Assets\_raid_reward.PNG',
    "r_sucess": 'Assets\_raid_sucess.PNG',
    "return_to_raids": 'Assets\_return_to_raids.PNG',
    "start_battle": 'Assets\_start_battle.PNG',
    "supp_req": 'Assets\_request_support.PNG',
    "go_to_my_page": 'Assets\_go_to_my_page.PNG',
    "r_events":'Assets\_raid_events.PNG',
    "r_regular":'Assets\_regular_raids.PNG',
    "item":'Assets\_use_item.PNG',
    "boss_available":'Assets\_raid_boss_available.PNG',
    "burst":'Assets\_burst_on.PNG'
    }
    return elements

def expected_buttons_rewards():
    elements= screen_elements()
    expected_buttons=[
    elements["r_reward"],
    elements["r_sucess"],
    elements["confirm"],
    elements["return_to_raids"]
    ]
    return expected_buttons

def scan_for_rewards():
    elements= screen_elements()
    expected_buttons=[
    elements["r_reward"],
    elements["r_sucess"]
    ]
    return expected_buttons


def expected_buttons_pre_battle():
    elements= screen_elements()
    expected_buttons=[
    elements["my_supp"],
    elements["confirm"],
    elements["to_quest"]
    ]
    return expected_buttons

def expected_buttons_in_battle():
    elements= screen_elements()
    expected_buttons=[
    elements["start_battle"],
    elements["supp_req"]
    ]
    return expected_buttons

def checking_ending():
    elements= screen_elements()
    expected_buttons=[
    elements["cancel"],
    elements["confirm"]
    
    ]
    return expected_buttons

def expected_buttons_in_ending():
    elements= screen_elements()
    expected_buttons=[
    elements["boss_available"],
    elements["go_to_my_page"],
    elements["confirm"],
    elements["return_to_raids"]
    ]
    return expected_buttons

def state_indicator():
    elements= screen_elements()
    expected_buttons=[
    elements["r_events"],
    elements["go_to_my_page"],
    elements["confirm"],
    elements["return_to_raids"]
    ]
    return expected_buttons


