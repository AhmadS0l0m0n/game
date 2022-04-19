import descriptions
import choices
import items

class Place:
    def __init__(self, name):
        self.name = name
        self.description = descriptions.DESCRIPTIONS[name]
        self.choices = choices.CHOICES[name]
        self.items = items.ITEMS[name]

    def take_item(self, item_name):
        try:
            if self.items[item_name] == 0:
                return ("You've already taken the " + item_name + "(s)", False)
            
            self.items[item_name] -= 1
            return ("You've taken the " + item_name, True)
            
        except:
            return ("You could not find a " + item_name, False)