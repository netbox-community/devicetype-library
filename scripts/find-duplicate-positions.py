# pip install pyyaml
# pip install levenshtein

import os, re, yaml
from collections import defaultdict
from itertools import groupby
from Levenshtein import distance

# Two module names with distance(name1, name2) > DISTANCE_THRESHHOLD are considered to be in different groups
DISTANCE_THRESHOLD = 2

def walk_device_type_files():
    root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "device-types")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if re.match(r'.+\.ya?ml$', file, re.IGNORECASE):
                full = os.path.join(root, file)
                rel = os.path.relpath(full, root_dir)
                yield full, rel

def get_bays_with_duplicate_positions(device_type):
    module_bays = device_type.get('module-bays')
    if module_bays is None:
        return

    # First, we filter out any module bays that have no position or no name
    module_bays = [bay for bay in module_bays if 'position' in bay and 'name' in bay]

    # Then, we sort by position so that itertools.groupby can do its thing,
    # and yield the groups, as long as there's at least 2 objects with the
    # same position.

    get_bay_position = lambda bay: bay['position']
    module_bays.sort(key=get_bay_position)
    for position, bays_iter in groupby(module_bays, get_bay_position):
        bay_names = [bay['name'] for bay in bays_iter]
        if len(bay_names) > 1:
            yield position, bay_names

def iter_pairs(items):
    count = len(items)
    for i, item1 in enumerate(items):
        for item2 in items[i+1:]:
            yield item1, item2

def iter_similar_pairs(strings, threshold=DISTANCE_THRESHOLD):
    for s1, s2 in iter_pairs(strings):
        if distance(s1, s2) <= threshold:
            yield s1, s2

for file_path, file_rel_path in walk_device_type_files():
    with open(file_path, 'r', encoding='utf8') as f:
        device_type = yaml.safe_load(f)
    for position, bay_names in get_bays_with_duplicate_positions(device_type):
        # Find any pairs of module bays with the same positions and similar names
        for bay1, bay2 in iter_similar_pairs(bay_names):
            print(f"In {file_rel_path}, module bays {bay1} and {bay2} both have position {position}.")
