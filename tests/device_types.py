import os


class DeviceType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path, change_type):
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
        self.change_type = change_type

    def _slugify_manufacturer(self):
        return self.manufacturer.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus-").replace("+", "-plus").replace("_", "-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-").replace("&", "and")

    def get_slug(self):
        if hasattr(self, "slug"):
            return self.slug
        return None

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-").replace("(", "").replace(")", "").replace(";", "")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def _slugify_part_number(self):
        slugified = self.part_number.casefold().replace(" ", "-").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-").replace("(", "").replace(")", "").replace(";", "")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def get_filepath(self):
        return self.file_path

    def verify_slug(self, KNOWN_SLUGS):
        # Verify the slug is unique, and not already known
        known_slug_list_intersect = [(slug, file_path) for slug, file_path in KNOWN_SLUGS if slug == self.slug]

        if len(known_slug_list_intersect) == 0:
            pass
        elif len(known_slug_list_intersect) == 1:
            if self.file_path not in known_slug_list_intersect[0][1]:
                if 'R' not in self.change_type:
                    self.failureMessage = f'{self.file_path} has a duplicate slug: "{self.slug}"'
                    return False
            return True
        else:
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
        KNOWN_SLUGS.add((self.slug, self.file_path))
        return True
    def validate_child_u_height(self):
        subdevice_role = self.definition.get('subdevice_role')
        u_height = self.definition.get('u_height', None)

        if subdevice_role == "child" and u_height != 0:
            self.failureMessage = f'{self.file_path} is a child device but has u_height={u_height}. Must be 0.'
            return False
        return True
    def validate_power(self):
        CUSTOM_POWER_SOURCE_PROPERTY = '_is_power_source'

        # Check if power-ports exists
        if self.definition.get('power-ports', False):
            # Verify that is_powered is not set to False. If so, there should not be any power-ports defined
            if not self.definition.get('is_powered', True):
                self.failureMessage = f'{self.file_path} has is_powered set to False, but "power-ports" are defined.'
                return False
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
                power_source = console_port.get(CUSTOM_POWER_SOURCE_PROPERTY, False)
                if power_source:
                    return True

        rear_ports = self.definition.get('rear-ports', False)
        if rear_ports:
            for rear_port in rear_ports:
                power_source = rear_port.get(CUSTOM_POWER_SOURCE_PROPERTY, False)
                if power_source:
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

        # As the very last case, check if is_powered is defined and is False. Otherwise assume the device is powered
        if not self.definition.get('is_powered', True): # is_powered defaults to True
            # Arriving here means is_powered is set to False, so verify that there are no power-outlets defined
            if self.definition.get('power-outlets', False):
                self.failureMessage = f'{self.file_path} has is_powered set to False, but "power-outlets" are defined.'
                return False
            return True

        self.failureMessage = f'{self.file_path} has does not appear to have a valid power source. Ensure either "power-ports" or "interfaces" with "poe_mode" is defined.'
        return False

    def ensure_no_vga(self):
        NO_VGA_COMPONENTS = [
            'console-ports',
            'console-server-ports',
            'interfaces',
            'front-ports',
            'rear-ports'
        ]

        for component_to_test in NO_VGA_COMPONENTS:
            test_component = self.definition.get(component_to_test, False)

            if test_component:
                for component in test_component:
                    name = component.get('name', "")
                    label = component.get('label', "")
                    if "vga" in name.casefold() or "vga" in label.casefold():
                        self.failureMessage = f'{self.file_path} has a VGA component defined. VGA is not a valid definition at this time.'
                        return False

        return True

class ModuleType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path, change_type):
        self.file_path = file_path
        self.isDevice = False
        self.definition = definition
        self.manufacturer = definition.get('manufacturer')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.part_number = definition.get('part_number', "")
        self._slug_part_number = self._slugify_part_number()
        self.change_type = change_type

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

class RackType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path, change_type):
        self.file_path = file_path
        self.isDevice = False
        self.definition = definition
        self.manufacturer = definition.get('manufacturer')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.change_type = change_type

    def get_filepath(self):
        return self.file_path

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

def validate_component_names(component_names: (set or None)):
    if len(component_names) > 1:
        verify_name = list(component_names[0])
        for index, name in enumerate(component_names):
            if index == 0:
                continue

            intersection = sorted(set(verify_name) & set(list(name)), key = verify_name.index)

            intersection_len = len(intersection)
            verify_subset = verify_name[:intersection_len]
            name_subset = list(name)[:intersection_len]
            subset_match = sorted(set(verify_subset) & set(name_subset), key = name_subset.index)

            if len(intersection) > 2 and len(subset_match) == len(intersection):
                return False
    return True

def verify_filename(device: (DeviceType or ModuleType or RackType), KNOWN_MODULES: (set or None)):
    head, tail = os.path.split(device.get_filepath())
    filename = tail.rsplit(".", 1)[0].casefold()

    # Check if file is RackType
    if "rack-types" in device.file_path:
        if not filename == device._slug_model:
            device.failureMessage = f'{device.file_path} file name is invalid. Must be the model "{device._slug_model}"'
            return False
        return True

    if not (filename == device._slug_model or filename == device._slug_part_number or filename == device.part_number.casefold()):
        device.failureMessage = f'{device.file_path} file name is invalid. Must be either the model "{device._slug_model}" or part_number "{device.part_number} / {device._slug_part_number}"'
        return False

    if not device.isDevice:
        matches = [file_name for file_name, file_path in KNOWN_MODULES if file_name.casefold() == filename.casefold()]
        if len(matches) > 1:
            device.failureMessage = f'{device.file_path} appears to be duplicated. Found {len(matches)} matches: {", ".join(matches)}'
            return False

    return True

def validate_components(component_types, device_or_module):
    for component_type in component_types:
        known_names = set()
        known_components = []
        defined_components = device_or_module.definition.get(component_type, [])
        if not isinstance(defined_components, list):
            device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type}.'
            return False
        for idx, component in enumerate(defined_components):
            if not isinstance(component, dict):
                device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type} ({idx}).'
                return False
            name = component.get('name')
            position = component.get('position')
            eval_component = (name, position)
            if not isinstance(name, str):
                device_or_module.failureMessage = f'{device_or_module.file_path} has an invalid definition for {component_type} name ({idx}).'
                return False
            if eval_component[0] in known_names:
                device_or_module.failureMessage = f'{device_or_module.file_path} has duplicated names within {component_type} ({name}).'
                return False
            known_components.append(eval_component)
            known_names.add(name)
            # Bi-directional POE validation for interfaces
            if component_type == "interfaces":
                poe_mode_present = "poe_mode" in component and bool(component["poe_mode"])
                poe_type_present = "poe_type" in component and bool(component["poe_type"])

                if poe_mode_present and not poe_type_present:
                    device_or_module.failureMessage = f'{device_or_module.file_path} has "poe_mode" defined in an interface without a matching "poe_type".'
                    return False
                if poe_type_present and not poe_mode_present:
                    device_or_module.failureMessage = f'{device_or_module.file_path} has "poe_type" defined in an interface without a matching "poe_mode".'
                    return False

        # Adding check for duplicate positions within a component type
        # Stems from https://github.com/netbox-community/devicetype-library/pull/1586
        # and from https://github.com/netbox-community/devicetype-library/issues/1584
        position_set = {}
        index = 0
        for name, position in known_components:
            if position is not None:
                match = []
                if len(position_set) > 0:
                    match = [key for key,val in position_set.items() if key == position]
                if len(match) == 0:
                    if len(position_set) == 0:
                        position_set = {position: {known_components[index]}}
                    else:
                        position_set.update({position: {known_components[index]}})
                else:
                    position_set[position].add(known_components[index])
            index = index + 1

        for position in position_set:
            if len(position_set[position]) > 1:
                component_names = [name for name,pos in position_set[position]]
                if not validate_component_names(component_names):
                    device_or_module.failureMessage = f'{device_or_module.file_path} has duplicated positions within {component_type} ({position}).'
                    return False

    return True
