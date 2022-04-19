#!/usr/bin/env python3
from math import ceil, floor
import pygame
import pygame_gui
import place

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import IncrementalThreadedResourceLoader, ObjectID
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED

from gamestate import GameState

"""
Font load time taken: 0.911 seconds.
Time taken 1st window: 1.509 seconds.
Time taken 2nd window: 0.181 seconds.
"""

def close_box(box):
    if box is not None:
        box.kill()
        
def create_health_bar(max_health, health):
    colors = ["#BFFF00", "#A4C639", "#C78B00", "#4d0b00"]
    percent = health/max_health
    color = colors[-1]
    if percent >= 0.75:
        color = colors[0]
    elif percent >= 0.5:
        color = colors[1]
    elif percent >= 0.25:
        color = colors[2]
    
    text = "<font color=" + color + ">|"
    part = ceil(percent * 10)
    for _ in range(0, part):
        text += "-"
    for _ in range(0, 10 - part):
        text += " "
    text += "|<font color=#FFFFFF>"
    return text

def create_character_description(character):
    return character.name + " [" + character.type + "] " + create_health_bar(character.max_health, character.health)

def create_battle_menu():
    return "<a href=\"menu1\">Attack</a><br><a href=\"menu2\">Inventory</a>"

def create_start_box():
    text1 = "<font color=#FF2937><b>Of Lords and Plagues</b><br><br>"
    text2 = "<a>Click to Start!</a>"
    return UITextBox(
            "<font face=fira_code pixel_size=90>" + text1 +
            "<font face=fira_code size=7>" + text2,
            pygame.Rect(10, 10, 780, 580),
            manager=ui_manager,
            object_id= ObjectID(class_id="@centered",
                                object_id="#text_box_2"))

def create_screen_box(text):
    return UITextBox(
            "<font face=fira_code size=5>" + text,
            pygame.Rect(10, 10, 780, 530),
            manager=ui_manager,
            object_id='#text_box_1')
    
def create_inventory_popup(text):
    return UITextBox(
            "<font face=fira_code size=5>" + text,
            pygame.Rect(10, 400, 700, 100),
            manager=ui_manager,
            object_id='#text_box_1')
    
def create_inventory_button(open = True):
    rect = pygame.Rect(0, 0, 300, 50)
    rect.bottomright = (-10, -10)
    return UITextBox(
            "<a href=\"open\"><font face=fira_code size=5>Click to open Inventory</a>"
            if open else "<a href=\"close\"><font face=fira_code size=5>Click to close Inventory</a>",
            rect,
            manager=ui_manager,
            object_id='#text_box_1',
            anchors={'left': 'right',
                    'right': 'right',
                    'top': 'bottom',
                    'bottom': 'bottom'})
    
def create_map_button(open = True):
    rect = pygame.Rect(0, 0, 300, 50)
    rect.bottomleft = (10, -10)
    return UITextBox(
            "<a href=\"open\"><font face=fira_code size=5>Click to open Map</a>"
            if open else "<a href=\"close\"><font face=fira_code size=5>Click to close Map</a>",
            rect,
            manager=ui_manager,
            object_id='#text_box_1',
            anchors={'left': 'left',
                    'right': 'left',
                    'top': 'bottom',
                    'bottom': 'bottom'})
    
def create_battle_box(text):
    return UITextBox(
            "<font face=fira_code size=5>" + text,
            pygame.Rect(10, 140, 780, 350),
            manager=ui_manager,
            object_id='#text_box_1')

def create_party_box(player_num):
    player = gamestate.party[player_num]
    text = create_character_description(player) + "<br>"
    return UITextBox(
            "<font face=fira_code size=5>" + text,
            pygame.Rect(10 + 390 * (player_num % 2), 490 + 50 * floor(player_num / 2), 390, 50),
            manager=ui_manager,
            object_id='#text_box_1')

def create_enemy_box(enemies = []):
    text = ""
    for enemy in enemies:
        text += create_character_description(enemy) + "<br>"
    return UITextBox(
            "<font face=fira_code size=5>" + text,
            pygame.Rect(10, 10, 780, 130),
            manager=ui_manager,
            object_id='#text_box_1')
    
def open_description_gui():
    global description_box
    global inventory_button
    global inventory_box
    close_box(inventory_box)
    close_box(description_box)
    description_box = create_screen_box(gamestate.description())
    close_box(inventory_button)
    inventory_button = create_inventory_button()
    
def open_inventory_gui():
    global description_box
    global inventory_box
    global inventory_button
    close_map()
    close_box(inventory_box)
    close_box(description_box)
    inventory_box = create_screen_box(gamestate.get_inventory_html())
    close_box(inventory_button)
    inventory_button = create_inventory_button(open = False)
    
def open_map():
    global map_button
    global description_box
    global popup_box
    close_box(popup_box)
    open_description_gui()
    close_box(description_box)
    gamestate.map_open = True
    close_box(map_button)
    map_button = create_map_button(open = False)
    
def close_map():
    global map_button
    global description_box
    open_description_gui()
    gamestate.map_open = False
    close_box(map_button)
    map_button = create_map_button()
    
def open_battle_gui():
    global map_button
    global description_box
    global popup_box
    global inventory_button
    global battle_box
    global party_boxes
    global enemy_box
    close_box(map_button)
    close_box(description_box)
    close_box(popup_box)
    close_box(inventory_button)
    battle_box = create_battle_box("A battle commences!")
    enemy_box = create_enemy_box(gamestate.battle.enemies)
    for i in range(0, len(gamestate.party)):
        party_boxes[i] = create_party_box(i)
        
def refresh_battle_gui(menu_text):
    global battle_box
    global party_boxes
    global enemy_box
    close_box(battle_box)
    close_box(enemy_box)
    battle_box = create_battle_box(menu_text)
    enemy_box = create_enemy_box(gamestate.battle.enemies)
    for i in range(0, len(gamestate.party)):
        close_box(party_boxes[i])
        party_boxes[i] = create_party_box(i)
    
    
def close_battle_gui():
    global map_button
    close_box(battle_box)
    close_box(enemy_box)
    for box in party_boxes:
        close_box(box)
    map_button = create_map_button()
    open_description_gui()
    
    

gamestate = GameState()
pygame.init()

pygame.display.set_caption("")
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

background_surface = pygame.Surface(screen_size)
background_surface.fill(pygame.Color("#000000"))

loader = IncrementalThreadedResourceLoader()
clock = pygame.time.Clock()

# Loading
ui_manager = UIManager(screen_size, 'theme_1.json', resource_loader=loader)
ui_manager.preload_fonts([
                          {'name': 'fira_code', 'html_size': 5, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 7, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 5, 'style': 'bold'},
                          {'name': 'fira_code', 'point_size': 90, 'style': 'bold'},
                          {'name': 'fira_code', 'point_size': 90, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 5, 'style': 'italic'}
                          ])
loader.start()
finished_loading = False
while not finished_loading:
    finished_loading, progress = loader.update()

# Keeping track of time
time_1 = clock.tick()
timer_1 = 0;
timer_2 = 0;

# Prepare the boxes
description_box = None

popup_box = None
inventory_button = create_inventory_button()
inventory_box = None

battle_box = None
party_boxes = [None, None, None, None]
enemy_box = None

map_button = create_map_button()
map_image = pygame.image.load("map.jpg")
map_image = pygame.transform.scale(map_image, (520, 520))
reticle_image = pygame.image.load("reticle.png")
reticle_image = pygame.transform.scale(reticle_image, (40, 40))

title_box = create_start_box()

# Game loop
running = True
while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == UI_TEXT_BOX_LINK_CLICKED:
            if event.ui_element is title_box:
                title_box.kill()
                create_screen_box(gamestate.description())
            
            if event.ui_element is description_box:
                choice_number = int(event.link_target) - 1
                choice_type, message = gamestate.choose(choice_number) #unsafe boundaries
                
                if choice_type == "move":
                    open_description_gui()
                elif choice_type == "give":
                    close_box(popup_box)
                    popup_box = create_inventory_popup(message)
                    timer_1 = 4
                elif choice_type == "battle":
                    open_battle_gui()
                    timer_2 = 2
                elif choice_type == "recruit":
                    close_box(popup_box)
                    popup_box = create_inventory_popup(message)
                    timer_1 = 4
                    
            elif event.ui_element is inventory_button:
                if event.link_target == "open":
                    open_inventory_gui()
                else:
                    open_description_gui()
                    
                    
            elif event.ui_element is map_button:
                if event.link_target == "open":
                    open_map()
                    
                else:
                    close_map()
                    
            elif event.ui_element is battle_box:
                
                if event.link_target.startswith("menu"):
                    if event.link_target == "menu1":
                        refresh_battle_gui(gamestate.battle.create_current_attack_list())
                    else:
                        refresh_battle_gui(gamestate.create_inventory_menu())
                        continue
                    
                elif event.link_target.startswith("attack"):
                    number = int(event.link_target.removeprefix("attack"))
                    if(number == 0):
                        refresh_battle_gui(create_battle_menu())
                    else:
                        gamestate.battle.current_attack = gamestate.battle.turn_order[0][1].moves[number-1]
                        refresh_battle_gui(gamestate.battle.create_enemy_menu())
                        
                elif event.link_target.startswith("enemy"):
                    number = int(event.link_target.removeprefix("enemy"))
                    if number == 0:
                        refresh_battle_gui(gamestate.battle.create_current_attack_list())
                    else:
                        success, end, item = gamestate.battle.take_turn(["attack", gamestate.battle.enemies[number-1], gamestate.battle.current_attack])
                        if end == None:
                            timer_2 = 2
                        elif end == "party":
                            gamestate.place = place.Place(gamestate.battle.end_location)
                            close_battle_gui()
                
                elif event.link_target.startswith("inventory"):
                    number = int(event.link_target.removeprefix("inventory"))
                    if number == 0:
                        refresh_battle_gui(create_battle_menu())
                    else:
                        gamestate.battle.current_item = list(gamestate.inventory.keys())[number - 1]
                        refresh_battle_gui(gamestate.battle.create_party_menu())
                        
                elif event.link_target.startswith("member"):
                    number = int(event.link_target.removeprefix("member"))
                    if number == 0:
                        refresh_battle_gui(gamestate.create_inventory_menu())
                    else:
                        success, end, item = gamestate.battle.take_turn(["use", gamestate.battle.party[number-1], gamestate.battle.current_item])
                        timer_2 = 2
                        if item is not None:
                            gamestate.add_item(item)

        ui_manager.process_events(event)

    if timer_1 > 0:
        timer_1 -= time_delta
        if timer_1 <= 0:
            close_box(popup_box)
            timer_1 = 0
    
    if timer_2 > 0:
        timer_2 -= time_delta
        if timer_2 <= 0:
            success, end, item = gamestate.battle.take_turn()
            if success:
                refresh_battle_gui(gamestate.battle.give_last_turn_description())
                timer_2 = 2
            elif end == "enemy":
                running = False
            else:
                refresh_battle_gui(create_battle_menu())
                timer_2 = 0
            

    screen.blit(background_surface, (0, 0))
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    if gamestate.map_open:
        screen.blit(map_image, (15, 15))
        screen.blit(reticle_image, gamestate.get_map_place())

    pygame.display.update()
