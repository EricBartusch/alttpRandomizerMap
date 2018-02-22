import json
import createAttributeMap
import getProgressiveItems

def get_seed(spoiler_data):
    for section, value in spoiler_data.items():
        if(section == "meta"):
            return value["seed"]  

SPOILER_DATA = json.load(open('testSpoiler.json'))
SEED = get_seed(SPOILER_DATA)

#Initialize constant information
#TODO: Move this outside whatever loop is used to go through files
PROGRESSIVE_ITEMS = getProgressiveItems.get_progressive_items(SPOILER_DATA)
ATTRIBUTE_MAP = createAttributeMap.create_attribute_map()

UNIQUE_ITEMS = ["Pegasus Boots", "Magic Powder", "Progessive Armor", "Lamp", "Bottle", "Magical Boomerang", "Bombos", \
 "Progressive Glove", "Moon Pearl", "Flippers", "Ice Rod", "Boomerang", "Half Magic", "Progressive Sword", "Cane of Byrna", \
 "Silver Arrows Upgrade", "Bug Catching Net", "Fire Rod", "Quake", "Book Of Mudora", "Progressive Shield", "Magic Mirror", "Magic Cape", \
 "Cane of Somaria", "Flute", "Ether", "Bow", "Hookshot", "Shovel", "Mushroom", "Bottle (Bee)", "Bottle (Golden Bee)", "Bottle (Red Potion)", \
 "Bottle (Green Potion)", "Bottle (Blue Potion)"]

#items people point out but aren't inheriently special
OTHER_INTERESTING_ITEMS = ["Heart Container (refill)", "One Rupee", "Arrow"]

NORMAL_ITEMS = ["Pice of Heart", "Twenty Rupees", "Three Hundred Rupees", "Three Bombs", "Five Rupees", "Fifty Rupees", "Arrow Upgrade (5)", \
"Ten Arrows", "Bomb Upgrade (10)", "Arrow Upgrade (10)", "Bomb Upgrade (5)"]

NON_DUNGEON_ITEMS = UNIQUE_ITEMS + OTHER_INTERESTING_ITEMS + NORMAL_ITEMS

#Loop through all items and create documents for their data
for section, value in SPOILER_DATA.items():
    if(section != "Special" and section != "playthrough" and section != "meta" and section != "Castle Tower"):
        for chest, item in value.items():
            if(item in non_dungeon_items):
                document = {}
                document["seed"] = SEED
                document["item"] = item
                document["location"] = chest
                document["progression"] = item in PROGRESSIVE_ITEMS
                document["unique"] = item in UNIQUE_ITEMS
                document["attributes"] = ATTRIBUTE_MAP[chest]
                with open("documents/" + str(SEED) + "-" + chest, "w", encoding='utf-8') as doc:
                    json.dump(document, doc, sort_keys=True, indent=4)
