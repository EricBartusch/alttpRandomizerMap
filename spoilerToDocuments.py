import json
import os
import sys
import argparse
import createAttributeMap
import getProgressiveItems
from collections import OrderedDict

def get_seed(spoiler_data):
    for section, value in spoiler_data.items():
        if(section == "meta"):
            return value["seed"]  

parser = argparse.ArgumentParser()
parser.add_argument('--doNormalItems')
parser.add_argument('--doDungeonItems')
args = parser.parse_args()

doNormalItems = int(args.doNormalItems)
doDungeonItems = int(args.doDungeonItems)

    
#Consistent information
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

#Elastic ID - needs to be unique for all items
for filename in os.listdir("spoilers"):
    #seed dependent info
    SPOILER_DATA = json.load(open("spoilers/" + filename))
    PROGRESSIVE_ITEMS = getProgressiveItems.get_progressive_items(SPOILER_DATA)
    SEED = get_seed(SPOILER_DATA)

    if doNormalItems:
        itemId = 0
        for section, value in SPOILER_DATA.items():
            if(section != "Special" and section != "playthrough" and section != "meta" and section != "Castle Tower"):
                for chest, item in sorted(value.items()):
                    if(item in NON_DUNGEON_ITEMS):
                        itemId += 1
                        indexId = {"index" : {"_id" : itemId}}
                        document = {}
                        document["seed"] = SEED
                        document["item"] = item
                        document["location"] = chest
                        document["progression"] = item in PROGRESSIVE_ITEMS
                        document["attrs"] = ATTRIBUTE_MAP[chest]
                        document["unique"] = item in UNIQUE_ITEMS
                        orderedDocument = OrderedDict(document)
                        with open("documents/" + str(SEED) + ".json", "a", encoding='utf-8') as doc:
                            json.dump(indexId, doc)
                            doc.write('\n')
                            json.dump(orderedDocument, doc)
                            doc.write('\n')
                            doc.close()

    if doDungeonItems:
        dungeonIndexId = 0
        for section, value in SPOILER_DATA.items():
            if(section != "Special" and section != "playthrough" and section != "meta" and section != "Castle Tower"):
                for chest, item in sorted(value.items()):
                    if(item not in NON_DUNGEON_ITEMS):
                        dungeonIndexId += 1
                        indexId = {"index" : {"_id" : dungeonIndexId}}
                        document = {}
                        document["seed"] = SEED
                        document["item"] = item
                        document["location"] = chest
                        document["progression"] = item in PROGRESSIVE_ITEMS
                        document["attrs"] = ATTRIBUTE_MAP[chest]
                        if("Big Key" in item):
                            document["attrs"].append("Big Key")
                        orderedDocument = OrderedDict(document)
                        with open("dungeonDocs/" + str(SEED) + "-dungeon.json", "a", encoding='utf-8') as doc:
                            json.dump(dungeonIndexId, doc)
                            doc.write('\n')
                            json.dump(orderedDocument, doc)
                            doc.write('\n')
                            doc.close()


