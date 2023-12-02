import os

def making_path(folder, path):
    fullpath = os.path.join(folder,path)
    return fullpath

def raid_boss_list():
    boss_folder='Assets//Raid_Boss//'
    name_list=[
    making_path(boss_folder,'phantom_T1.PNG'),

    making_path(boss_folder,'dark_T6.PNG'),
    making_path(boss_folder,'thunder_T6.PNG'),

    making_path(boss_folder,'dark_T5.PNG'),
    making_path(boss_folder,'light_T5.PNG'),
    making_path(boss_folder,'wind_T5.PNG'),
    making_path(boss_folder,'thunder_T5.PNG'),  
    making_path(boss_folder,'water_T5.PNG'),   
    making_path(boss_folder,'fire_T5.PNG'),
    
    making_path(boss_folder,'dark_T4.PNG'),
    making_path(boss_folder,'light_T4.PNG'),
    making_path(boss_folder,'wind_T4.PNG'),
    making_path(boss_folder,'thunder_T4.PNG'),  
    making_path(boss_folder,'water_T4.PNG'),    
    making_path(boss_folder,'fire_T4.PNG'),
    
    making_path(boss_folder,'dark_T3.PNG'),
    making_path(boss_folder,'light_T3.PNG'),
    making_path(boss_folder,'wind_T3.PNG'),
    making_path(boss_folder,'thunder_T3.PNG'),  
    making_path(boss_folder,'water_T3.PNG'),    
    making_path(boss_folder,'fire_T3.PNG'),

    making_path(boss_folder,'dark_T2.PNG'),
    #making_path(boss_folder,'light_T2.PNG'),
    making_path(boss_folder,'wind_T2.PNG'),
    making_path(boss_folder,'thunder_T2.PNG'),  
    #making_path(boss_folder,'water_T2.PNG'),
    #making_path(boss_folder,'fire_T2.PNG'),

    making_path(boss_folder,'dark_T1.PNG'),
    #making_path(boss_folder,'light_T1.PNG'),
    making_path(boss_folder,'wind_T1.PNG'),
    making_path(boss_folder,'thunder_T1.PNG'),  
    making_path(boss_folder,'water_T1.PNG'),   
    making_path(boss_folder,'fire_T1.PNG'),
    
    ]
    return name_list

def screen_elements():
    screen_verification_folder="Assets\\Verification_assets\\"
    screen_assets_folder="Assets\\Screen_assets\\"

    
    elements = {

    "battle_lost":  making_path(screen_verification_folder, 'scrn_raid_lost.PNG'),
    "battle_gu":  making_path(screen_verification_folder, 'scrn_give_up.PNG'),
    "battle_won":  making_path(screen_verification_folder, 'scrn_mvp.PNG'),
    "boss_available": making_path(screen_assets_folder, 'raid_boss_available.PNG'),
    "burst": making_path(screen_assets_folder, 'burst_on.PNG'),

    "cancel":  making_path(screen_assets_folder,'cancel.PNG'),
    "challenge": making_path(screen_assets_folder, 'challange_raid.PNG'),
    "confirm":  making_path(screen_assets_folder, 'confirm.PNG'),

    "daily_raid_begin": making_path(screen_assets_folder, 'raid_begin.PNG'),
    "down": making_path(screen_assets_folder, 'list_down.PNG'),
    
    "go_to_quest": making_path(screen_assets_folder, 'go_to_quest.png'),
    "go_to_my_page":  making_path(screen_assets_folder, 'go_to_my_page.PNG'),

    "item": making_path(screen_assets_folder, 'use_item.PNG'),

    "mid_battle":  making_path(screen_verification_folder, 'scrn_refresh.PNG'),
    "my_supp":  making_path(screen_assets_folder, 'my_supp.png'),

    "notice": making_path(screen_verification_folder, 'scrn_notice.PNG'),
    "No_btt": making_path(screen_assets_folder, 'no_battles.PNG'),

    "popup":  making_path(screen_verification_folder, 'scrn_close_popup.PNG'),

    "raid_quests": making_path(screen_assets_folder, 'raid_quests.PNG'),
    "request_support":  making_path(screen_verification_folder, 'scrn_request_supp.PNG'),
    "retry": making_path(screen_assets_folder, 'retry.PNG'),
    "return_to_raids":  making_path(screen_assets_folder, 'return_to_raids.PNG'),
    "r_reward": making_path(screen_assets_folder, 'raid_reward.PNG') ,
    "r_sucess":  making_path(screen_assets_folder, 'raid_sucess.PNG'),
    "r_events": making_path(screen_assets_folder, 'raid_events.PNG'),
    "r_regular": making_path(screen_assets_folder, 'regular_raids.PNG'),

    "select_raid": making_path(screen_verification_folder, 'scrn_list_raids_1.PNG'),
    "select_supp": making_path(screen_verification_folder, 'support_eindolons.PNG'),
    "start_battle": making_path(screen_assets_folder, 'start_battle.PNG') ,
    "supp_req": making_path(screen_assets_folder, 'request_support.PNG') ,

    "up": making_path(screen_assets_folder, 'list_up.PNG'),

    }
    return elements

def verification_elements():
    elements= screen_elements()
    S_elements = [
        elements["select_raid"],
        elements["select_supp"],
        elements["request_support"],
        elements["battle_lost"],
        elements["battle_gu"],
        elements["mid_battle"],
        elements["battle_won"],
        elements["popup"]

    ]
    return S_elements

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

