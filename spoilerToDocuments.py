import json
import createAttributeMap

def get_progressive_items(data):
    """
    Gets all the items from the 'playthrough' section
    """
    progressive_items = list()
    for section, value in data.items():
        if(section == "playthrough"):
            for step, location in value.items():
                if(type(location) is dict):
                    for chest, itemList in location.items():
                        for item in itemList.values():
                            if("Big Key" not in item and "Crystal" not in item and "Defeat" not in item and "Pendant" not in item):
                                progressive_items.append(item)

    return progressive_items  

def get_seed(data):
    for section, value in data.items():
        if(section == "meta"):
            return value["seed"]  

data = json.load(open('testSpoiler.json'))

progressive_items = get_progressive_items(data)
attribute_map = createAttributeMap.create_attribute_map()

#get seed number
seed = get_seed(data)

unique_items = ["Pegasus Boots", "Magic Powder", "Progessive Armor", "Lamp", "Bottle", "Magical Boomerang", "Bombos", \
 "Progressive Glove", "Moon Pearl", "Flippers", "Ice Rod", "Boomerang", "Half Magic", "Progressive Sword", "Cane of Byrna", \
 "Silver Arrows Upgrade", "Bug Catching Net", "Fire Rod", "Quake", "Book Of Mudora", "Progressive Shield", "Magic Mirror", "Magic Cape", \
 "Cane of Somaria", "Flute", "Ether", "Bow", "Hookshot", "Shovel", "Mushroom", "Bottle (Bee)", "Bottle (Golden Bee)", "Bottle (Red Potion)", \
 "Bottle (Green Potion)", "Bottle (Blue Potion)"]

#items people point out but aren't inheriently special
other_interesting_items = ["Heart Container (refill)", "One Rupee", "Arrow"]

normal_items = ["Pice of Heart", "Twenty Rupees", "Three Hundred Rupees", "Three Bombs", "Five Rupees", "Fifty Rupees", "Arrow Upgrade (5)", \
"Ten Arrows", "Bomb Upgrade (10)", "Arrow Upgrade (10)", "Bomb Upgrade (5)"]

non_dungeon_items = unique_items + other_interesting_items + normal_items

#Loop through all items and create documents for thier data
for section, value in data.items():
    if(section != "Special" and section != "playthrough" and section != "meta" and section != "Castle Tower"):
        for chest, item in value.items():
            if(item in non_dungeon_items):
                document = {}
                document["seed"] = seed
                document["item"] = item
                document["location"] = chest
                document["progression"] = item in progressive_items
                document["unique"] = item in unique_items
                document["attributes"] = attribute_map[chest]
                with open("documents/" + str(seed) + "-" + chest, "w", encoding='utf-8') as doc:
                    json.dump(document, doc, sort_keys=True, indent=4)
