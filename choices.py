CHOICES = {
    "Start": [
        ["move", "The King", None],
    ],
    "The King": [
        ["give", "Treasure Chest"],
        ["move", "Hills", None],
    ],
    "Hills": [
        ["move", "Narrow Path", None],
        ["move", "Fork", 
            {
                "Chance": 1,
                "Enemies": {
                    "Bandit": 2
                }
            }
         ],
    ],
    "Narrow Path": [
        ["recruit", "Battle Wolf"],
        ["move", "The Tower", None],
        ["move", "Hills", None]
    ],
    "Fork": [
        ["give", "Stuff"],
        ["move", "Hills", None],
    ],
    "The Tower": [
        ["move", "The Hall", 
            {
                "Chance": 1,
                "Enemies": {
                    "Mistress of War": 1
                }
            }
        ],
        ["move", "Narrow Path", None]
    ],
    "The Hall": [
        ["move", "The End", 
            {
                "Chance": 1,
                "Enemies": {
                    "Lord of Pestilence": 1
                }
            }
        ]
    ],
    "The End": []
}