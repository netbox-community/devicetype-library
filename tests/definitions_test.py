from test_configuration import COMPONENT_TYPES, IMAGE_FILETYPES, SCHEMAS, SCHEMAS_BASEPATH, KNOWN_SLUGS, ROOT_DIR, USE_LOCAL_KNOWN_SLUGS, NETBOX_DT_LIBRARY_URL, KNOWN_MODULES, USE_UPSTREAM_DIFF, PRECOMMIT_ALL_SWITCHES
import pickle_operations
from yaml_loader import DecimalSafeLoader
from device_types import DeviceType, ModuleType, RackType, verify_filename, validate_components
import decimal
import glob
import json
import os
import tempfile
import psutil
from urllib.request import urlopen
import pytest
import yaml
from referencing import Registry, Resource
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from git import Repo

def _get_definition_files():
    """
    Return a list of all definition files within the specified path.
    """
    file_list = []

    for path, schema in SCHEMAS:
        # Initialize the schema
        with open(f"schema/{schema}") as schema_file:
            schema = json.loads(schema_file.read(), parse_float=decimal.Decimal)

        # Validate that the schema exists
        assert schema, f"Schema definition for {path} is empty!"

        # Map each definition file to its schema as a tuple (file, schema)
        for file in sorted(glob.glob(f"{path}/*/*", recursive=True)):
            file_list.append((file, schema, 'skip'))

    return file_list

def _generate_schema_registry():
    """
    Return a list of all definition files within the specified path.
    """
    registry = Registry()

    for schema_f in os.listdir(SCHEMAS_BASEPATH):
        # Initialize the schema
        with open(f"schema/{schema_f}") as schema_file:
            resource = Resource.from_contents(json.loads(schema_file.read(), parse_float=decimal.Decimal))
            registry = resource @ registry

    return registry

def _get_diff_from_upstream():
    file_list = []

    repo = Repo(f"{os.path.dirname(os.path.abspath(__file__))}/../")
    commits_list = list(repo.iter_commits())

    if "upstream" not in repo.remotes:
        repo.create_remote("upstream", NETBOX_DT_LIBRARY_URL)

    upstream = repo.remotes.upstream
    upstream.fetch()
    changes = upstream.refs.master.commit.diff(repo.head)
    changes = changes + repo.index.diff("HEAD")

    for path, schema in SCHEMAS:
        # Initialize the schema
        with open(f"schema/{schema}") as schema_file:
            schema = json.loads(schema_file.read(), parse_float=decimal.Decimal)

        # Validate that the schema exists
        assert schema, f"Schema definition for {path} is empty!"

        # Ensure files are either added, renamed, modified or type changed (do not get deleted files)
        CHANGE_TYPE_LIST = ['A', 'R', 'M', 'T']

        # Iterate through changed files
        for file in changes:
            # Ensure the files are modified or added, this will disclude deleted files
            if file.change_type in CHANGE_TYPE_LIST:
                # If the file is renamed, ensure we are picking the right schema
                if 'R' in file.change_type and path in file.rename_to:
                    file_list.append((file.rename_to, schema, file.change_type))
                elif path in file.a_path:
                    file_list.append((file.a_path, schema, file.change_type))
                elif path in file.b_path:
                    file_list.append((file.b_path, schema, file.change_type))

    return file_list

def _get_image_files():
    """
    Return a list of all image files within the specified path and manufacturer.
    """
    file_list = []

    # Map each image file to its manufacturer
    for file in sorted(glob.glob(f"elevation-images{os.path.sep}*{os.path.sep}*", recursive=True)):
        # Validate that the file extension is valid
        assert file.split(os.path.sep)[2].split('.')[-1] in IMAGE_FILETYPES, f"Invalid file extension: {file}"

        # Map each image file to its manufacturer as a tuple (manufacturer, file)
        file_list.append((file.split(os.path.sep)[1], file))

    return file_list

def _decimal_file_handler(uri):
    """
    Handler to work with floating decimals that fail normal validation.
    """
    with urlopen(uri) as url:
        result = json.loads(url.read().decode("utf-8"), parse_float=decimal.Decimal)
    return result

def test_environment():
    """
    Run basic sanity checks on the environment to ensure tests are running correctly.
    """
    # Validate that definition files exist
    if definition_files:
        pytest.skip("No changes to definition files found.")

EVALUATE_ALL = False
if any(x in PRECOMMIT_ALL_SWITCHES for x in psutil.Process(os.getppid()).cmdline()):
    EVALUATE_ALL = True

if USE_UPSTREAM_DIFF and not EVALUATE_ALL:
    definition_files = _get_diff_from_upstream()
else:
    definition_files = _get_definition_files()
image_files = _get_image_files()

if USE_LOCAL_KNOWN_SLUGS:
    KNOWN_SLUGS = pickle_operations.read_pickle_data(f'{ROOT_DIR}/tests/known-slugs.pickle')
    KNOWN_MODULES = pickle_operations.read_pickle_data(f'{ROOT_DIR}/tests/known-modules.pickle')
    KNOWN_RACKS = pickle_operations.read_pickle_data(f'{ROOT_DIR}/tests/known-racks.pickle')
else:
    temp_dir = tempfile.TemporaryDirectory()
    repo = Repo.clone_from(url=NETBOX_DT_LIBRARY_URL, to_path=temp_dir.name)
    KNOWN_SLUGS = pickle_operations.read_pickle_data(f'{temp_dir.name}/tests/known-slugs.pickle')
    KNOWN_MODULES = pickle_operations.read_pickle_data(f'{temp_dir.name}/tests/known-modules.pickle')
    KNOWN_RACKS = pickle_operations.read_pickle_data(f'{ROOT_DIR}/tests/known-racks.pickle')

SCHEMA_REGISTRY = _generate_schema_registry()

@pytest.mark.parametrize(('file_path', 'schema', 'change_type'), definition_files)
def test_definitions(file_path, schema, change_type):
    """
    Validate each definition file using the provided JSON schema and check for duplicate entries.
    """
    # Check file extension. Only .yml or .yaml files are supported.
    assert file_path.split('.')[-1] in ('yaml', 'yml'), f"Invalid file extension: {file_path}"

    # Read file
    with open(file_path) as definition_file:
        content = definition_file.read()

    # Check for trailing newline. YAML files must end with an emtpy newline.
    assert content.endswith('\n'), "Missing trailing newline"

    # Load YAML data from file
    definition = yaml.load(content, Loader=DecimalSafeLoader)

    # Check for non-ASCII characters
    non_ascii_chars = [char for char in content if ord(char) > 127]
    if non_ascii_chars:
        pytest.fail(
            f"{file_path} contains non-ASCII characters: {', '.join(set(non_ascii_chars))}",
            pytrace=False
        )

    # Validate YAML definition against the supplied schema
    try:
        # Validate definition against schema
        validator = Draft202012Validator(schema, registry=SCHEMA_REGISTRY)
        validator.validate(definition)
    except ValidationError as e:
        # Schema validation failure. Ensure you are following the proper format.
        pytest.fail(f"{file_path} failed validation: {e}", False)

    # Identify if the definition is for a Device or Module
    if "device-types" in file_path:
        # A device
        this_device = DeviceType(definition, file_path, change_type)
    elif "module-types" in file_path:
        # A module type
        this_device = ModuleType(definition, file_path, change_type)
    elif "rack-types" in file_path:
        # A rack type
        this_device = RackType(definition, file_path, change_type)
    else:
        # A module
        this_device = ModuleType(definition, file_path, change_type)

    # Validate that front-ports reference existing rear-ports
    if any(x in file_path for x in ("device-types", "module-types")):
        rear_ports = definition.get("rear-ports", []) or []
        front_ports = definition.get("front-ports", []) or []

        rear_port_names = {
            rp.get("name") for rp in rear_ports if isinstance(rp, dict)
        }

        for fp in front_ports:
            if not isinstance(fp, dict):
                continue

            rear_port_ref = fp.get("rear_port")

            if rear_port_ref and rear_port_ref not in rear_port_names:
                pytest.fail(
                    f"{file_path}: front-port '{fp.get('name')}' references "
                    f"rear_port '{rear_port_ref}', but no such rear-port exists. "
                    f"Defined rear-ports: {sorted(rear_port_names)}",
                    pytrace=False,
                )

    # Verify the slug is valid, only if the definition type is a Device
    if this_device.isDevice:
        assert this_device.verify_slug(KNOWN_SLUGS), pytest.fail(this_device.failureMessage, False)

    # Verify the filename is valid. Must either be the model or part_number.
    assert verify_filename(this_device, (KNOWN_MODULES if not this_device.isDevice else None)), pytest.fail(this_device.failureMessage, False)

    # Check for duplicate components within the definition
    assert validate_components(COMPONENT_TYPES, this_device), pytest.fail(this_device.failureMessage, False)

    # Check for empty quotes and fail if found
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

    # Check for valid power definitions
    if this_device.isDevice:
        assert this_device.validate_power(), pytest.fail(this_device.failureMessage, False)
        assert this_device.ensure_no_vga(), pytest.fail(this_device.failureMessage, False)
        assert this_device.validate_child_u_height(), pytest.fail(this_device.failureMessage, False)

    # Check for images if front_image or rear_image is True
    if (definition.get('front_image') or definition.get('rear_image')):
        # Find images for given manufacturer, with matching device slug (exact match including case)
        manufacturer_images = [image[1] for image in image_files if image[0] == file_path.split(os.path.sep)[1] and os.path.basename(image[1]).split('.')[0] == this_device.get_slug()]
        if not manufacturer_images:
            pytest.fail(f'{file_path} has Front or Rear Image set to True but no images found for manufacturer/device (slug={this_device.get_slug()})', False)
        elif len(manufacturer_images)>2:
            pytest.fail(f'More than 2 images found for device with slug {this_device.get_slug()}: {manufacturer_images}', False)

        # If front_image is True, verify that a front image exists
        if(definition.get('front_image')):
            front_image = [image_path.split('/')[2] for image_path in manufacturer_images if os.path.basename(image_path).split('.')[1] == 'front']

            if not front_image:
                pytest.fail(f'{file_path} has front_image set to True but no matching image found (looking for \'elevation-images{os.path.sep}{file_path.split(os.path.sep)[1]}{os.path.sep}{this_device.get_slug()}.front.ext\' but only found {manufacturer_images})', False)

        # If rear_image is True, verify that a rear image exists
        if(definition.get('rear_image')):
            rear_image = [image_path.split('/')[2] for image_path in manufacturer_images if os.path.basename(image_path).split('.')[1] == 'rear']

            if not rear_image:
                pytest.fail(f'{file_path} has rear_image set to True but no matching image found (looking for \'elevation-images{os.path.sep}{file_path.split(os.path.sep)[1]}{os.path.sep}{this_device.get_slug()}.rear.ext\' but only found {manufacturer_images})', False)
    iterdict(definition)
