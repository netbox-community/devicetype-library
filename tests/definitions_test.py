import glob
import json
import os
import pytest
import yaml
from jsonschema import validate, RefResolver, Draft4Validator
from jsonschema.exceptions import ValidationError


SCHEMAS = (
    ('device-types', 'devicetype.json'),
    ('module-types', 'moduletype.json'),
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
        for f in glob.glob(f"{path}/*/*", recursive=True):
            ret.append((f, schema))

    return ret


definition_files = _get_definition_files()


def test_environment():
    """
    Run basic sanity checks on the environment to ensure tests are running correctly.
    """
    # Validate that definition files exist
    assert definition_files, "No definition files found!"


@pytest.mark.parametrize(('file_path', 'schema'), definition_files)
def test_definitions(file_path, schema):
    """
    Validate each definition file using the provided JSON schema.
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

    try:
        resolver = RefResolver(f'file://{os.getcwd()}/schema/devicetype.json', schema)
        Draft4Validator(schema, resolver=resolver).validate(definition)
    except ValidationError as e:
        pytest.fail(f"{file_path} failed validation: {e}", False)
