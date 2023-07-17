from test_configuration import KNOWN_SLUGS
import os

class DeviceType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path):
        self.file_path = file_path
        self.isDevice = True
        self.definition = definition
        self.manufacturer = definition.get('manufacturer')
        self._slug_manufacturer = self._slugify_manufacturer()
        self.slug = definition.get('slug')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.part_number = definition.get('part_number', "")
        self._slug_part_number = self._slugify_part_number()
        self.failureMessage = None

    def _slugify_manufacturer(self):
        return self.manufacturer.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus-").replace("+", "-plus").replace("_", "-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-").replace("&", "and")

    def get_slug(self):
        if hasattr(self, "slug"):
            return self.slug
        return None

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def _slugify_part_number(self):
        slugified = self.part_number.casefold().replace(" ", "-").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def get_filepath(self):
        return self.file_path

    def verify_slug(self):
        # Verify the slug is unique, and not already known
        if self.slug in KNOWN_SLUGS:
            self.failureMessage = f'{self.file_path} has a duplicate slug "{self.slug}"'
            return False

        # Verify the manufacturer is appended to the slug
        if not self.slug.startswith(self._slug_manufacturer):
            self.failureMessage = f'{self.file_path} contains slug "{self.slug}". Does not start with manufacturer: "{self.manufacturer.casefold()}-"'
            return False

        # Verify the slug ends with either the model or part number
        if not (self.slug.endswith(self._slug_model) or self.slug.endswith(self._slug_part_number)):
            self.failureMessage = f'{self.file_path} has slug "{self.slug}". Does not end with the model "{self._slug_model}" or part_number "{self._slug_part_number}"'
            return False

        # Add the slug to the list of known slugs
        KNOWN_SLUGS.add(self.slug)
        return True

    def validate_power(self):
        # Check if power-ports exists
        if self.definition.get('power-ports', False):
            return True

        # Lastly, check if interfaces exists and has a poe_mode defined
        interfaces = self.definition.get('interfaces', False)
        if interfaces:
            for interface in interfaces:
                poe_mode = interface.get('poe_mode', "")
                if poe_mode != "" and poe_mode == "pd":
                    return True

        console_ports = self.definition.get('console-ports', False)
        if console_ports:
            for console_port in console_ports:
                poe = console_port.get('poe', "")
                if poe != "" and poe is True:
                    return True

        # Check if the device is a child device, and if so, assume it has a valid power source from the parent
        subdevice_role = self.definition.get('subdevice_role', False)
        if subdevice_role:
            if subdevice_role == "child":
                return True

        # Check if module-bays exists
        if self.definition.get('module-bays', False):
            # There is not a standardized way to define PSUs that are module bays, so we will just assume they are valid
            return True

        self.failureMessage = f'{self.file_path} has does not appear to have a valid power source. Ensure either "power-ports" or "interfaces" with "poe_mode" is defined.'
        return False

class ModuleType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path):
        self.file_path = file_path
        self.isDevice = False
        self.definition = definition
        self.manufacturer = definition.get('manufacturer')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.part_number = definition.get('part_number', "")
        self._slug_part_number = self._slugify_part_number()

    def get_filepath(self):
        return self.file_path

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def _slugify_part_number(self):
        slugified = self.part_number.casefold().replace(" ", "-").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

def verify_filename(device: (DeviceType or ModuleType)):
    head, tail = os.path.split(device.get_filepath())
    filename = tail.rsplit(".", 1)[0].casefold()

    if not (filename == device._slug_model or filename == device._slug_part_number or filename == device.part_number.casefold()):
        device.failureMessage = f'{device.file_path} file name is invalid. Must be either the model "{device._slug_model}" or part_number "{device.part_number} / {device._slug_part_number}"'
        return False

    return True

def validate_components(component_types, device_or_module):
    for component_type in component_types:
        known_names = set()
        defined_components = device_or_module.definition.get(component_type, [])
        if not isinstance(defined_components, list):
            device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type}.'
            return False
        for idx, component in enumerate(defined_components):
            if not isinstance(component, dict):
                device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type} ({idx}).'
                return False
            name = component.get('name')
            if not isinstance(name, str):
                device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type} name ({idx}).'
                return False
            if name in known_names:
                device_or_module.failureMessage = f'{device_or_module.file_path} has duplicated names within {component_type} ({name}).'
                return False
            known_names.add(name)

    return True
