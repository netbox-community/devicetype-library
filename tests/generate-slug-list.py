import os
import json
import glob
import yaml
import decimal
from yaml_loader import DecimalSafeLoader
from jsonschema import Draft4Validator, RefResolver
from jsonschema.exceptions import ValidationError
from test_configuration import SCHEMAS, KNOWN_SLUGS, ROOT_DIR
from urllib.request import urlopen
import pickle_operations

def _get_device_type_files():
    """
    Return a list of all definition files within the specified path.
    """
    file_list = []

    for path, schema in SCHEMAS:
        if path == 'device-types':
            # Initialize the schema
            with open(f"{ROOT_DIR}/schema/{schema}") as schema_file:
                schema = json.loads(schema_file.read(),
                                    parse_float=decimal.Decimal)

            # Validate that the schema exists
            if not schema:
              print(f"Schema definition for {path} is empty!")
              exit(1)

            # Map each definition file to its schema as a tuple (file, schema)
            for file in sorted(glob.glob(f"{path}/*/*", recursive=True)):
                file_list.append((f'{file}', schema))

    return file_list

def _decimal_file_handler(uri):
    """
    Handler to work with floating decimals that fail normal validation.
    """
    with urlopen(uri) as url:
        result = json.loads(url.read().decode("utf-8"), parse_float=decimal.Decimal)
    return result

def load_file(file_path, schema):
    # Read file
    try:
        with open(file_path) as definition_file:
            content = definition_file.read()
    except Exception as exc:
        return (False, f'Error opening "{file_path}". stderr: {exc}')

    # Check for trailing newline. YAML files must end with an emtpy newline.
    if not content.endswith('\n'):
      return (False, f'{file_path} is missing trailing newline')

    # Load YAML data from file
    try:
        definition = yaml.load(content, Loader=DecimalSafeLoader)
    except Exception as exc:
        return (False, f'Error during yaml.load "{file_path}". stderr: {exc}')

    # Validate YAML definition against the supplied schema
    try:
        resolver = RefResolver(
            f"file://{os.getcwd()}/schema/devicetype.json",
            schema,
            handlers={"file": _decimal_file_handler},
        )
        # Validate definition against schema
        Draft4Validator(schema, resolver=resolver).validate(definition)
    except ValidationError as exc:
        # Schema validation failure. Ensure you are following the proper format.
        return (False, f'{file_path} failed validation: {exc}')

    return (True, definition)

def _generate_known_slugs():
    all_files = _get_device_type_files()

    for file_path, schema in all_files:
        definition_status, definition = load_file(file_path, schema)
        if not definition_status:
            print(definition)
            exit(1)

        KNOWN_SLUGS.add((definition.get('slug'), file_path))

_generate_known_slugs()
pickle_operations.write_pickle_data(KNOWN_SLUGS, f'{ROOT_DIR}/tests/known-slugs.pickle')