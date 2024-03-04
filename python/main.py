import argparse
import json
import pprint
import aggregation as ag
import filter as fil
from typing import Dict, List, Tuple

Aggregation = Tuple[str, int]


def run(data: List[dict], models: List[str], properties: List[str]) -> Dict[str, List[Aggregation]]:
    """
    Takes a list of entity objects, filters data matching the `models` and `properties` specifications,
    and then aggregates the data returning a sorted list of aggregations.

    :param data: The list entity data
    :param models: A list of models to filter the aggregation on
    :param properties: A list of property keys and values to filter the aggregation on. Format:
        key:value1,value2
    """
    filtered_data = fil.filter_data(data, models, properties)
    aggregrate = ag.aggregate_data(filtered_data, models, properties)
    return aggregrate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # support `extend` action for python versions less than 3.8
    class ExtendAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr(namespace, self.dest) or []
            items.extend(values)
            setattr(namespace, self.dest, items)

    parser.register("action", "extend", ExtendAction)
    parser.add_argument("-i", "--input-file", default="entity.json", help="The data file to be processed.")
    parser.add_argument(
        "-m",
        "--models",
        # stores a list, and extends each argument value to the list
        action="extend",
        default=list(),
        nargs="*",
        help="Model(s) to include.",
    )
    parser.add_argument(
        "-p",
        "--properties",
        # stores a list, and extends each argument value to the list
        action="extend",
        default=list(),
        nargs="*",
        help="""
        Properties to filter on.
        Assumes no key has ':' or ' ' and no property has ','. Format key:value1,value2
        """,
    )
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        data = json.load(f)

    pprint.pprint(run(data, args.models, args.properties))
