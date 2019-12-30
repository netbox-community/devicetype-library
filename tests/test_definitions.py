import glob
import json
import pytest
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def _get_definition_files():
    """
    Return a list of all definition files.
    """
    return [f for f in glob.glob("device-types/*/*", recursive=True)]


# Initialize schema
with open("tests/schema.json") as schema_file:
    schema = json.loads(schema_file.read())


def test_environment():
    """
    Run basic sanity checks on the environment to ensure tests are running correctly.
    """
    # Validate that definition files exist
    assert _get_definition_files(), "No definition files found!"

    # Validate that the schema exists
    assert schema, "Schema definition is empty!"


@pytest.mark.parametrize("file_path", _get_definition_files())
def test_definition(file_path):
    """
    Validate each DeviceType definition file using the provided JSON schema.
    """
    # Check file extension
    assert file_path.split('.')[-1] in ('yaml', 'yml'), f"Invalid file extension: {file_path}"

    # Read file
    with open(file_path) as definition_file:
        content = definition_file.read()

        # Check for trailing newline
        assert content[-1] == '\n', "Missing trailing newline"

        # Load YAML data
        definition = yaml.load(content, Loader=yaml.SafeLoader)

    # Run validation
    try:
        validate(definition, schema=schema)
    except ValidationError as e:
        pytest.fail(f"{file_path} failed validation: {e}")
