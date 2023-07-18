import os

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

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

KNOWN_SLUGS = set()