import glob
import json
import pytest
import yaml

KNOWN_MODELS = {}

def _get_definition_files():
    """
    Return a list of all definition files.
    """
    return [f for f in glob.glob("device-types/*/*", recursive=True)]

def test_environment():
    """
    Run basic sanity checks on the environment to ensure tests are running correctly.
    """
    # Validate that definition files exist
    assert _get_definition_files(), "No definition files found!"

@pytest.mark.parametrize("file_path", _get_definition_files())
def test_dupes(file_path):
    # Check file extension
    assert file_path.split('.')[-1] in ('yaml', 'yml'), f"Invalid file extension: {file_path}"

    # Read file
    with open(file_path) as definition_file:
        content = definition_file.read()

        # Check for trailing newline
        assert content[-1] == '\n', "Missing trailing newline"

        # Load YAML data
        definition = yaml.load(content, Loader=yaml.SafeLoader)

    slug = definition.get('slug')

    if KNOWN_MODELS.get(slug, None) is not None:
        pytest.fail(f"{file_path} is a duplicate device_type for {slug}")

    KNOWN_MODELS[slug] = definition.get('model')
