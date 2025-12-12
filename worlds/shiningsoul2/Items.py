from BaseClasses import Item, ItemClassification

class SS2Item(Item):
    game = "Shining Soul 2"

SS2_ITEM_TABLE = {
    #"Unlock Goblin Fort": 0x52001,
    "Unlock Granny": 0x52002,
    "Unlock Granny Well": 0x52003,
    "Unlock Graveyard": 0x52004,
    "Unlock Palace": 0x52005,
    "Unlock Fairy Spring": 0x52006,
    "Unlock Pirate Ship": 0x52007,
    "Unlock Desert": 0x52008,
    "Unlock Cave": 0x52009,
    "Unlock Demon Tower": 0x5200A,
    "Unlock Volcano": 0x5200B,
    "Unlock Chaos Castle": 0x5200C,
    "Defeat Chaos": 0x5200D,
}

SS2_UNLOCK_FLAGS = {
    #"Unlock Goblin Fort":   (0x0202D5D4, 0),  # Bit 0 - already set at game start
    "Unlock Graveyard":     (0x0202D5D4, 1),  # Bit 1 - set after Goblin Fort
    "Unlock Palace":        (0x0202D5D4, 2),  # Bit 2 - set after Graveyard
    "Unlock Fairy Spring":  (0x0202D5D4, 3),  # Bit 3 - set after Palace
    "Unlock Pirate Ship":   (0x0202D5D4, 4),  # Bit 4 - set after Fairy Spring
    "Unlock Desert":        (0x0202D5D4, 5),  # Bit 5 - set after Pirate Ship (also sets D5D5 bit 5)
    "Unlock Cave":          (0x0202D5D4, 6),  # Bit 6 - set after Desert
    "Unlock Demon Tower":   (0x0202D5D4, 7),  # Bit 7 - set after Cave
    "Unlock Volcano":       (0x0202D5D5, 0),  # Bit 0 - set after Demon Tower
    "Unlock Chaos Castle":  (0x0202D5D5, 1),  # Bit 1 - set after Volcano
    "Unlock Granny Well":   (0x0202D5D6, 1),  # Bit 1
}

SS2_ITEMS = list(SS2_ITEM_TABLE.keys())

def make_item(name, player):
    return SS2Item(name, ItemClassification.progression, SS2_ITEM_TABLE[name], player)