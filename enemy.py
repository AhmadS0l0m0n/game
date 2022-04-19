from math import floor
import random
import enemies
import damage_types
class Enemy:
    def __init__(self, name):
        enemy = enemies.ENEMIES[name]
        self.name = name
        self.max_health = self.health = enemy["Health"]
        self.type = enemy["Type"]
        self.moves = enemy["Moves"]
        self.armor = enemy["Armor"]
        
    def attack(self):
        random.shuffle(self.moves)
        return self.moves[0]
    
    def get_hit(self, attack):
        base_damage = attack["Damage"]
        damage_type = attack["Type"]
        type_multiplier = 1
        if self.type in damage_types.DAMAGE_TYPES[damage_type]:
            type_multiplier = damage_types.DAMAGE_TYPES[damage_type][self.type]
        armor_multiplier = 100 / self.armor
        base_multiplier = 1
        
        self.health -= floor(base_multiplier * base_damage * type_multiplier * armor_multiplier)
        if self.health < 0:
            return False
        return True
        