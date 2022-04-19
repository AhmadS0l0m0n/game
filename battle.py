import random
import enemy
import enemies

class Battle:
    def __init__(self, party, enemies_list, end_location):
        self.turn_order = []
        self.end_location = end_location
        self.party = party
        self.enemies = []
        self.last_turn = ["Nobody", "Anything"]
        self.current_attack = None
        self.current_item = None
        for enemy_instance in enemies_list:
            if enemy_instance == "Any":
                for _ in range(0, enemies_list[enemy_instance]):
                    name = random.choice(list(enemies.ENEMIES.keys()))
                    self.enemies.append(enemy.Enemy(name))
                    self.turn_order.append(["enemy", self.enemies[-1]])
            else:
                for _ in range(0, enemies_list[enemy_instance]):
                    self.enemies.append(enemy.Enemy(enemy_instance))
                    self.turn_order.append(["enemy", self.enemies[-1]])
        for member in party:
            self.turn_order.append(["member", member])
        random.shuffle(self.turn_order)
        
    def take_turn(self, action = None):
        if self.turn_order[0][0] == "member" and action == None:
            return False, None, None
        
        first = self.turn_order[0]
        self.turn_order.pop(0)
        self.turn_order.append(first)
        
        if first[0] == "enemy":
            attack = first[1].attack()
            self.last_turn = [first[1].name, attack["Name"]]
            random.shuffle(self.party)
            member_alive = self.party[0].get_hit(attack)
            if not member_alive:
                to_remove = self.party[0]
                try:
                    self.party.pop(0)
                    self.turn_order.remove(to_remove)
                except: 
                    pass
            if len(self.party) == 0:
                return True, "enemy"
            return True, None, None
        
        if action[0] == "use":
            item_return = action[1].use(action[2])
            return True, None, item_return
            
        if action[0] == "attack":
            enemy_alive = action[1].get_hit(action[2])    
            if not enemy_alive:
                to_remove = action[1]
                try:
                    self.enemies.remove(to_remove)
                    self.turn_order.remove(to_remove)
                except:
                    pass
        
        if len(self.enemies) == 0:
            return True, "party", None
        
        return True, None, None
    
    def give_last_turn_description(self):
        return self.last_turn[0] + " used " + self.last_turn[1] + "!"
    
    def give_move_description(self, move):
        return move["Name"] + " [" + move["Type"] + "] " + str(move["Damage"])
        
    def create_current_attack_list(self):
        text = ""
        curr_member = self.turn_order[0][1]
        for i in range(0, len(curr_member.moves)):
            text += "<a href=\"attack" + str(i + 1) + "\">" + self.give_move_description(curr_member.moves[i]) + "</a><br>"
        text += "<a href=\"attack0\">Back</a><br>"
        return text
    
    def create_party_menu(self):
        text = ""
        for i in range(0, len(self.party)):
            text += "<a href=\"member" + str(i + 1) + "\">" + self.party[i].name + "</a><br>"
        text += "<a href=\"member0\">Back</a><br>"
        return text
    
    def create_enemy_menu(self):
        text = ""
        for i in range(0, len(self.enemies)):
            text += "<a href=\"enemy" + str(i + 1) + "\">" + self.enemies[i].name + "</a><br>"
        text += "<a href=\"enemy0\">Back</a><br>"
        return text
            
        