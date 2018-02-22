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