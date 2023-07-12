from test_configuration import KNOWN_SLUGS
import os

class DeviceType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path):
        self.file_path = file_path
        self.isDevice = True
        self.manufacturer = definition.get('manufacturer')
        self._slug_manufacturer = self._slugify_manufacturer()
        self.slug = definition.get('slug')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.part_number = definition.get('part_number', "")
        self._slug_part_number = self._slugify_part_number()
        self.failureMessage = None

    def get_manufacturer(self):
        return self.manufacturer

    def _slugify_manufacturer(self):
        return self.manufacturer.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus-").replace("+", "-plus").replace("_", "-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-").replace("&", "and")

    def get_slug(self):
        if hasattr(self, "slug"):
            return self.slug
        return None

    def get_model(self):
        return self.model

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

    def get_part_number(self):
        return self.part_number

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
            self.failureMessage = f'{self.file_path} device type has duplicate slug "{self.slug}"'
            return False

        # Verify the manufacturer is appended to the slug
        if not self.slug.startswith(self._slug_manufacturer):
            self.failureMessage = f'{self.file_path} device type has slug "{self.slug}" which does not start with manufacturer "{self.manufacturer}"'
            return False

        # Verify the slug ends with either the model or part number
        if not (self.slug.endswith(self._slug_model) or self.slug.endswith(self._slug_part_number)):
            self.failureMessage = f'{self.file_path} has slug "{self.slug}". Does not end with the model "{self._slug_model}" or part number "{self._slug_part_number}"'
            return False

        # Add the slug to the list of known slugs
        KNOWN_SLUGS.add(self.slug)
        return True

class ModuleType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path):
        self.file_path = file_path
        self.isDevice = False
        self.manufacturer = definition.get('manufacturer')
        self.model = definition.get('model')
        self._slug_model = self._slugify_model()
        self.part_number = None
        self._slug_part_number = None

    def get_manufacturer(self):
        return self.manufacturer

    def get_filepath(self):
        return self.file_path

    def _slugify_model(self):
        slugified = self.model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
        if slugified.endswith("-"):
            slugified = slugified[:-1]
        return slugified

def verify_filename(device: (DeviceType or ModuleType)):
    head, tail = os.path.split(device.get_filepath())
    filename = tail.rsplit(".", 1)[0].casefold()

    if not (filename == device._slug_model or filename == device._slug_part_number):
        device.failureMessage = f'{device.file_path} file is not either the model "{device._slug_model}" or part_number "{device._slug_part_number}"'
        return False

    return True