
import pprint
from typing import Dict, List, Tuple

Aggregation = Tuple[str, int]

def aggregate_data(data: List[dict], models: List[str], properties: List[str]) -> Dict[str, List[Aggregation]]:
    result = {}
    for datum in data:
        # iterate over models to aggregate
        for model in models:
            if model == datum["model"]:
                for property in datum["properties"]:
                    if property["slug"] not in result:
                        result[property["slug"]] = dict()
                    if property["value"] not in result[property["slug"]]:
                        result[property["slug"]][property["value"]] = 0
                    result[property["slug"]][property["value"]] += 1
    aggr = {}
    for k, value in result.items():
        aggr[k] = list()
        for key, v in value.items():
            new_item = (key, v)
            aggr[k].append(new_item)
        # sort on count
        aggr[k].sort(key=lambda x:(x[1]) , reverse=True)
    return aggr