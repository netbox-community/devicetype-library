import os
from urllib.parse import urlparse

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

# Source the upstream clone/fetch URL from the environment (so CI or a maintainer can
# override it) with the canonical upstream as the default, then validate it strictly.
# A pull request must not be able to point the harness's git clone/fetch at an arbitrary
# host (SSRF) or a non-upstream repo (validation-data substitution) — GHSA-8cfp-3c4q-xr6x.
def _resolve_netbox_dt_library_url():
    url = os.environ.get(
        "DTL_NETBOX_DT_LIBRARY_URL",
        "https://github.com/netbox-community/devicetype-library.git",
    )
    parsed = urlparse(url)
    allowed_paths = (
        "/netbox-community/devicetype-library",
        "/netbox-community/devicetype-library.git",
    )
    if (parsed.scheme != "https"
            or parsed.hostname != "github.com"
            or parsed.path.rstrip("/") not in allowed_paths):
        raise ValueError(
            f"Refusing untrusted NETBOX_DT_LIBRARY_URL {url!r}: it must be "
            "https://github.com/netbox-community/devicetype-library(.git)."
        )
    return url

NETBOX_DT_LIBRARY_URL = _resolve_netbox_dt_library_url()
