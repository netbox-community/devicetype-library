import glob
import json
import os
import pytest
import yaml
import warnings
from jsonschema import RefResolver, Draft4Validator
from jsonschema.exceptions import ValidationError


SCHEMAS = (
    ('device-types', 'devicetype.json'),
    ('module-types', 'moduletype.json'),
)

COMPONENT_TYPES = (
    'console-ports',
    'console-server-ports',
    'power-ports',
    'power-outlets',
    'interfaces',
    'front-ports',
    'rear-ports',
    'device-bays',
    'module-bays',
)


def _get_definition_files():
    """
    Return a list of all definition files within the specified path.
    """
    ret = []

    for path, schema in SCHEMAS:

        # Initialize the schema
        with open(f"schema/{schema}") as schema_file:
            schema = json.loads(schema_file.read())

        # Validate that the schema exists
        assert schema, f"Schema definition for {path} is empty!"

        # Map each definition file to its schema
        for f in sorted(glob.glob(f"{path}/*/*", recursive=True)):
            ret.append((f, schema))

    return ret


definition_files = _get_definition_files()
known_slugs = set()


def test_environment():
    """
    Run basic sanity checks on the environment to ensure tests are running correctly.
    """
    # Validate that definition files exist
    assert definition_files, "No definition files found!"


@pytest.mark.parametrize(('file_path', 'schema'), definition_files)
def test_definitions(file_path, schema):
    """
    Validate each definition file using the provided JSON schema and check for duplicate entries.
    """
    # Check file extension
    assert file_path.split('.')[-1] in ('yaml', 'yml'), f"Invalid file extension: {file_path}"

    # Read file
    with open(file_path) as definition_file:
        content = definition_file.read()

    # Check for trailing newline
    assert content.endswith('\n'), "Missing trailing newline"

    # Load YAML data from file
    definition = yaml.load(content, Loader=yaml.SafeLoader)

    # Validate YAML definition against the supplied schema
    try:
        resolver = RefResolver(f'file://{os.getcwd()}/schema/devicetype.json', schema)
        Draft4Validator(schema, resolver=resolver).validate(definition)
    except ValidationError as e:
        pytest.fail(f"{file_path} failed validation: {e}", False)

    # Check for duplicate slug
    if file_path.startswith('device-types/'):
        slug = definition.get('slug')
        if slug and slug in known_slugs:
            pytest.fail(f'{file_path} device type has duplicate slug "{slug}"', False)
        elif slug:
            known_slugs.add(slug)

    # Check for duplicate components
    for component_type in COMPONENT_TYPES:
        known_names = set()
        defined_components = definition.get(component_type, [])
        for idx, component in enumerate(defined_components):
            name = component.get('name')
            if name in known_names:
                pytest.fail(f'Duplicate entry "{name}" in {component_type} list', False)
            known_names.add(name)

    # Check for "other" in component types
    for component_type in COMPONENT_TYPES:
        defined_components = definition.get(component_type, [])
        for idx, component in enumerate(defined_components):
            name = component.get('name')
            type = component.get('type')
            if type == "other":
                warnings.warn(SyntaxWarning(f'Type is "other" for interface {name}'))

    # Check for empty quotes
    def iterdict(var):
        for dict_value in var.values():
            if isinstance(dict_value, dict):
                iterdict(dict_value)
            if isinstance(dict_value, list):
                iterlist(dict_value)
            else:
                if(isinstance(dict_value, str) and not dict_value):
                    pytest.fail(f'{file_path} has empty quotes', False)

    def iterlist(var):
        for list_value in var:
            if isinstance(list_value, dict):
                iterdict(list_value)
            elif isinstance(list_value, list):
                iterlist(list_value)

    iterdict(definition)
