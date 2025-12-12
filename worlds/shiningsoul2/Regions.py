from worlds.generic.Rules import set_rule
from BaseClasses import Region, Entrance

def create_regions(world, player, locations):
    # Create the two regions
    menu = Region("Menu", player, world)
    ss2_region = Region("Shining Soul 2", player, world)

    world.regions += [menu, ss2_region]

    menu_to_ss2 = Entrance(player, "Menu → Shining Soul 2", menu)
    menu.exits.append(menu_to_ss2)
    menu_to_ss2.connect(ss2_region)

    for loc_name, loc_id in locations.items():
        ss2_region.add_location(world.create_location(player, loc_name, loc_id))

    return
