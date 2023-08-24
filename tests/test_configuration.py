import os

__all__ = (
    'SCHEMAS',
    'IMAGE_FILETYPES',
    'COMPONENT_TYPES',
    'ROOT_DIR',
    'KNOWN_SLUGS',
    'KNOWN_MODULES',
    'USE_LOCAL_KNOWN_SLUGS',
    'USE_UPSTREAM_DIFF',
    'NETBOX_DT_LIBRARY_URL',
)

SCHEMAS = (
    ('device-types', 'devicetype.json'),
    ('module-types', 'moduletype.json'),
)

IMAGE_FILETYPES = (
    'bmp', 'gif', 'pjp', 'jpg', 'pjpeg', 'jpeg', 'jfif', 'png', 'tif', 'tiff', 'webp'
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

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

KNOWN_SLUGS = set()
KNOWN_MODULES = set()

USE_LOCAL_KNOWN_SLUGS = os.environ.get('USE_LOCAL_KNOWN_SLUGS', False)
USE_UPSTREAM_DIFF = os.environ.get('CI', False)

NETBOX_DT_LIBRARY_URL = "https://github.com/netbox-community/devicetype-library.git"
