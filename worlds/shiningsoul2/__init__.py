from .Client import ShiningSoul2Client
from .Items import SS2_ITEM_TABLE, SS2_ITEMS, make_item
from .Locations import SS2_LOCATION_TABLE, SS2_LOCATIONS, SS2Location
from worlds.AutoWorld import World
from BaseClasses import Region

class ShiningSoul2World(World):
    game = "Shining Soul 2"
    topology_present = False
    romfiletype = "gba"

    item_name_to_id = SS2_ITEM_TABLE
    location_name_to_id = SS2_LOCATION_TABLE

    def get_rom_filetype(self):
        return "gba"

    def modify_rom(self, rom):
        return

    def create_item(self, name):
        return make_item(name, self.player)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        stages = Region("Stages", self.player, self.multiworld)
        for loc in SS2_LOCATIONS:
            loc_id = SS2_LOCATION_TABLE[loc]
            stages.locations.append(SS2Location(self.player, loc, loc_id, stages))
        self.multiworld.regions += [menu, stages]
        menu.connect(stages)

    def create_items(self):
        for name in SS2_ITEMS:
            self.multiworld.itempool.append(self.create_item(name))

    def set_rules(self):
        # Victory when Kill Chaos location is reached
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.can_reach_location("Kill Chaos", self.player)
        )

    def fill_slot_data(self):
        return {}
