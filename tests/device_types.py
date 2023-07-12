class DeviceType:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, definition, file_path):
        self.file_path = file_path
        self.manufacturer = definition.get('manufacturer')
        if file_path.startswith('device-types/'):
          self.slug = definition.get('slug')

    def get_manufacturer(self):
      return self.manufacturer

    def get_slug(self):
      if hasattr(self, "slug"):
        return self.slug
      return None

    def get_filepath(self):
      return self.file_path
