# NetBox Device Type Library

## About this Library

This library is intended to be used for populating device types in [NetBox](https://github.com/netbox-community/netbox)
version 2.7 or later. It contains a set of device type definitions expressed in YAML and arranged by manufacturer. Each
file represents a discrete physical device type (e.g. make and model). These definitions can be loaded into NetBox to
obviate the need to create device types and their associated components manually.

If you would like to contribute to this library, please read through our [contributing guide](CONTRIBUTING.md) before 
submitting content.

If you would like to automate the import of these devicetype template files, there is a **community based** python script 
that will check for duplicates, allow you to only import specific vendors, etc. available here [minitriga/Netbox-Dvice-Type-Library-Import](https://github.com/minitriga/Netbox-Device-Type-Library-Import). Note: it is not related to Netbox in any official way and you will not get support for it here.

## Device Type Definitions

Each definition must include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this device type.
- `model`: The model number of the device type. This must be unique per manufacturer.
- `slug`: A URL-friendly representation of the model number. Like the model number, this must be unique per
  manufacturer.

The following fields may optionally be declared:

- `part_number`: An alternative representation of the model number (e.g. a SKU).
- `u_height`: The height of the device type in rack units. (Default: 1)
- `is_full_depth`: A boolean which indicates whether the device type consumes both the front and rear rack faces.
  (Default: true)
- `subdevice_role`: Indicates that this is a `parent` or `child` device. (Default: None)

For further detail on these attributes and those listed below, please reference the
[schema definition](tests/schema.json).

### Component Definitions

Valid component types are listed below. Each type of component must declare a list of the individual component templates
to be added.

- `console-ports`
- `console-server-ports`
- `power-ports`
- `power-outlets`
- `interfaces`
- `rear-ports`
- `front-ports`
- `device-bays`

The available fields for each type of component are listed below.

#### Console Ports

- `name`: Port name
- `type`: Port type slug (API value)

#### Console Server Ports

- `name`: Port name
- `type`: Port type slug (API value)

#### Power Ports

- `name`: Port name
- `type`: Port type slug (API value)
- `maximum_draw`: The port's maximum power draw, in watts (optional)
- `allocated_draw`: The port's allocated power draw, in watts (optional)

#### Power Outlets

- `name`: Outlet name
- `type`: Port type slug (API value)
- `power_port`: The name of the power port on the device which powers this outlet (optional)
- `feed_leg`: The phase (leg) of power to which this outlet is mapped; A, B, or C (optional)

#### Interfaces

- `name`: Interface name
- `type`: Interface type slug (API value)
- `mgmt_only`: A boolean which indicates whether this interface is used for management purposes only (default: false)

#### Front Ports

- `name`: Port name
- `type`: Port type slug (API value)
- `rear_port`: The name of the rear port on this device to which the front port maps
- `rear_port_position`: The corresponding position on the mapped rear port (default: 1)

#### Rear Ports

- `name`: Port name
- `type`: Port type slug (API value)
- `positions`: The number of front ports that can map to this rear port (default: 1)

#### Device Bays

- `name`: Bay name

## Data Validation / Commit Quality Checks

There are two ways this repo focuses on keeping quality device-type definitions:

- Pre-Commit Checks - Optional for helping to identify simple issues before committing. (trailing-whitespace, end-of-file-fixer, check-yaml, yamlfmt, yamllint)
  - [Install pre-commit](https://pre-commit.com/#install) (or just use the requirements.txt file)
  - To install the pre-commit script `pre-commit install`
  - To run the pre-commit script on changed files `pre-commit run`
  - To run the pre-commit script on all files `pre-commit run --all`
  - To uninstall the pre-commit script `pre-commit uninstall`
  - Learn more about [pre-commit](https://pre-commit.com/)
- GitHub Actions - Automatically run before a PR can be merged.  Repeats yamllint & validates against NetBox Device-Type Schema.

