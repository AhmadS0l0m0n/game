import random
import member
import place
import coordinates
import battle
import item_bundles

class GameState:
    def __init__(self):
        self.place = place.Place("Start")
        self.party = [member.Member("The Knight", self)]
        self.inventory = {}
        self.battle = None
        self.map_open = False
        
    def add_party_member(self, name):
        self.party.append(member.Member(name, self))    
    
    def start_battle(self, end_location, enemies):
        self.battle = battle.Battle(self.party, enemies, end_location)
        
    def description(self):
        return self.place.description
        
    def choose(self, option_number):
        choice = self.place.choices[option_number]
        message = ""
        if choice[0] == "give":
            message = self.add_item(choice[1])
        
        elif choice[0] == "move":
            if choice[2] is not None:
                if choice[2]["Chance"] >= random.random():
                    self.start_battle(choice[1], choice[2]["Enemies"])
                    return ("battle", choice[1])
            
            self.place = place.Place(choice[1])
            
        elif choice[0] == "recruit":
            self.add_party_member(choice[1])
            message = "You've recruited " + choice[1] + "!"
        
        return (choice[0], message)
    
    def remove_item(self, item_name):
        try:
            item_amount = self.inventory[item_name]
            self.inventory[item_name] = item_amount - 1
        except KeyError:
            pass
        
        if self.inventory[item_name] == 0:
            self.inventory.pop(item_name, None)
    
    def add_item(self, item_name):
        message, success = self.place.take_item(item_name)
        if not success: 
            return message
        
        if item_name in item_bundles.ITEM_BUNDLES:
            message = "Taken the "
            for item_type in item_bundles.ITEM_BUNDLES[item_name]:
                message += item_type + "(s) <br>and the "
                try:
                    item_amount = self.inventory[item_type]
                    self.inventory[item_type] = item_amount + item_bundles.ITEM_BUNDLES[item_name][item_type]
                except KeyError:
                    self.inventory[item_type] = item_bundles.ITEM_BUNDLES[item_name][item_type]
            message = message.removesuffix(" <br>and the ")
            return message
                
        try:
            item_amount = self.inventory[item_name]
            self.inventory[item_name] = item_amount + 1
        except KeyError:
            self.inventory[item_name] = 1
        
        return message
    
    def get_inventory_html(self):
        result = ""
        for item in self.inventory:
            result += item + ": " + str(self.inventory[item]) + "<br>"
        return result
    
    def get_map_place(self):
        return coordinates.COORDS[self.place.name]
    
    def create_inventory_menu(self):
        text = ""
        for i in range(0, len(list(self.inventory.keys()))):
            text += "<a href=\"inventory" + str(i + 1) + "\">" + list(self.inventory.keys())[i] + " (" + str(list(self.inventory.values())[i]) + ")</a><br>"
        text += "<a href=\"inventory0\">Back</a><br>"
        return text