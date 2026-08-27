import json


def write_known_data(data, file_path):
    """
    Serialize a set of tuples (e.g. (slug, file_path)) to JSON.

    JSON is used instead of pickle because pickle executes arbitrary code on
    load (CWE-502), and these cache files are tracked in git and read by the
    test suite. The data is sorted so the on-disk output is deterministic and
    produces clean diffs. A slug may be None, so the sort key coerces each
    element to str to avoid TypeError when comparing None with str.

    A trailing newline is written so the generated file is already in the
    fixed point of the end-of-file-fixer pre-commit hook; without it the hook
    (or an editor) would append one after generation and create spurious diffs.
    """
    with open(file_path, 'w') as json_file:
        json.dump(
            sorted(data, key=lambda item: tuple(str(element) for element in item)),
            json_file,
            indent=0,
        )
        json_file.write('\n')


def read_known_data(file_path):
    """
    Read JSON-serialized known data back into a set of tuples.

    JSON has no tuple or set types: tuples are stored as arrays and would be
    loaded as lists, so each item is converted back to a tuple before being
    placed in a set (lists are unhashable and would raise TypeError).
    """
    with open(file_path) as json_file:
        return set(tuple(item) for item in json.load(json_file))
