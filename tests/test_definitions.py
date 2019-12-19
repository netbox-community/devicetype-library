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
    return [f for f in glob.glob("vendors/**/*.yaml", recursive=True)]


# Initialize schema
with open("tests/schema.json") as schema_file:
    schema = json.loads(schema_file.read())


@pytest.mark.parametrize("file_path", _get_definition_files())
def test_definition(file_path):
    """
    Validate DeviceType definitions using the provided JSON schema.
    """
    # Read file
    with open(file_path) as definition_file:
        definition = yaml.load(definition_file.read(), Loader=yaml.SafeLoader)

    # Run validation
    try:
        validate(definition, schema=schema)
    except ValidationError as e:
        pytest.fail(f"{file_path} failed validation: {e}")
