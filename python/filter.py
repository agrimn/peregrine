from typing import Dict, List, Tuple

Aggregation = Tuple[str, int]

def filter_data(data: List[dict], models: List[str], properties: List[str]) -> List[dict]:
    filtered_data = list()
    
    for datum in data:
        # first filter on models 
        if models:
            for m in models:
                if datum["model"] == m:
                    # now check on properties 
                    if has_property(datum, properties):
                        filtered_data.append(datum)
        else:
            # in no model filter is specified
            if has_property(datum, properties):
                filtered_data.append(datum)
    return filtered_data

def has_property(datum: dict, properties: List[str]) -> bool:
    result = True
    for property in properties:
        split = property.split(":")
        for datum_property in datum["properties"]:
            if datum_property["slug"] == split[0]:
                # check for multiple properties
                if "," in split[1]:
                    local_compare = False
                    compare_values = split[1].split(",")
                    for c in compare_values:
                        compare = getCorrectType(datum_property["type"], c)
                        if datum_property["value"] == compare:
                            local_compare = True
                            break
                    result = local_compare
                else:
                    compare = getCorrectType(datum_property["type"], split[1])
                    if datum_property["value"] != compare:
                        return False
    return result

def getCorrectType(type:str, value: str):
    match type:
        case "boolean":
            return value == 'True'
        case "integer":
            return int(value)
        case _:
            return value