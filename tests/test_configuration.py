import os

SCHEMAS = (
    ('device-types', 'devicetype.json'),
    ('module-types', 'moduletype.json'),
    ('rack-types', 'racktype.json'),
)
SCHEMAS_BASEPATH = f"{os.getcwd()}/schema/"

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

PRECOMMIT_ALL_SWITCHES = [
  '-a',
  '--all-files',
  '--all'
]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

KNOWN_SLUGS = set()
KNOWN_MODULES = set()
KNOWN_RACKS = set()

# Read the slug/module/rack caches from the locally committed JSON files (the
# fast path) only when a developer explicitly opts in via the environment, e.g.
# `DTL_USE_LOCAL_KNOWN_SLUGS=1 pytest`. Sourcing this from the environment rather
# than a tracked constant means a pull request cannot flip it on in CI.
USE_LOCAL_KNOWN_SLUGS = os.environ.get("DTL_USE_LOCAL_KNOWN_SLUGS") == "1"
USE_UPSTREAM_DIFF = True

NETBOX_DT_LIBRARY_URL = "https://github.com/netbox-community/devicetype-library.git"
