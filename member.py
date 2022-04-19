from math import floor
import party
import damage_types
import item_uses

class Member:
    def __init__(self, name, state):
        member = party.PARTY[name]
        self.name = name
        self.max_health = self.health = member["Health"]
        self.type = member["Type"]
        self.moves = member["Moves"]
        self.armor = member["Armor"]
        self.equipment = None
        self.state = state
        
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
    
    def use(self, item):
        use = item_uses.ITEM_USES[item]
        item_return = None
        if use[0] == "Heal":
            self.health = min(self.health + use[1], self.max_health)
            
        if use[0] == "Armor":
            item_return = self.equipment
            self.equipment = item
            if item_return in item_uses.ITEM_USES:
                self.armor -= item_uses.ITEM_USES[item_return][1]
            self.armor += use[1]
        
        self.state.remove_item(item)
        
        return item_return
                
        