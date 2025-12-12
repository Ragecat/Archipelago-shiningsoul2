from BaseClasses import Location

class SS2Location(Location):
    game = "Shining Soul 2"

SS2_LOCATION_TABLE = {
    "Goblin Fort Clear": 0x51001,
    "Talked to Granny": 0x51002,
    "Granny Well Clear": 0x51003,
    "Graveyard Clear": 0x51004,
    "Palace Clear": 0x51005,
    "Fairy Spring Clear": 0x51006,
    "Pirate Ship Clear": 0x51007,
    "Desert Clear": 0x51008,
    "Cave Clear": 0x51009,
    "Demon Tower Clear": 0x5100A,
    "Volcano Clear": 0x5100B,
    "Chaos Castle Clear": 0x5100C,
    "Kill Chaos": 0x5100D,
}

SS2_LOCATIONS = list(SS2_LOCATION_TABLE.keys())

SS2_CLEAR_FLAGS = {
    "Goblin Fort Clear":    (0x0202D5D0, 0),  # D5D0: 00->01 (bit 0)
    "Talked to Granny":     (0x0202D5D6, 1),  # D5D6: 00->02 (bit 1)
    "Granny Well Clear":    (0x0202D5D2, 1),  # D5D2: 00->02 (bit 1) - (happens after talking to granny again post-clear)
    "Graveyard Clear":      (0x0202D5D0, 1),  # D5D0: 01->03 (bit 1)
    "Palace Clear":         (0x0202D5D0, 2),  # D5D0: 03->07 (bit 2)
    "Fairy Spring Clear":   (0x0202D5D0, 3),  # D5D0: 07->0F (bit 3)
    "Pirate Ship Clear":    (0x0202D5D0, 4),  # D5D0: 0F->1F (bit 4)
    "Desert Clear":         (0x0202D5D0, 5),  # D5D0: 1F->3F (bit 5)
    "Cave Clear":           (0x0202D5D0, 6),  # D5D0: 3F->7F (bit 6)
    "Demon Tower Clear":    (0x0202D5D1, 0),  # D5D1: 00->01 (bit 0)
    "Volcano Clear":        (0x0202D5D1, 1),  # D5D1: 01->03 (bit 1)
    "Chaos Castle Clear":   (0x0202D5D1, 1),  # D5D1: 01->03 (bit 1)
    "Kill Chaos":           (0x0202D5D1, 4),  # D5D1: 03->13 (bit 4)
}