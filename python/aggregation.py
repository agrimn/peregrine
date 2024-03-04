
import pprint
from typing import Dict, List, Tuple

Aggregation = Tuple[str, int]

def aggregate_data(data: List[dict]) -> Dict[str, List[Aggregation]]:
    result = {}
    for datum in data:
        # iterate over models to aggregate
        if datum["model"] not in result:
            result[datum["model"]] = dict()
        for property in datum["properties"]:
            if property["slug"] not in result[datum["model"]]:
                result[datum["model"]][property["slug"]] = dict()
            if property["value"] not in result[datum["model"]][property["slug"]]:
                result[datum["model"]][property["slug"]][property["value"]] = 0
            result[datum["model"]][property["slug"]][property["value"]] += 1
    aggr = {}
    for m, model in result.items():
        for k, value in model.items():
            aggr[k] = list()
            for key, v in value.items():
                new_item = (key, v)
                aggr[k].append(new_item)
            # sort on count
            aggr[k].sort(key=lambda x:(x[1]) , reverse=True)
    return aggr
