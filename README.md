# NetBox Device Type Library

## About this Library

This library is intended to be used for populating device types in [NetBox](https://github.com/netbox-community/netbox).
It contains a set of device type definitions expressed in YAML and arranged by manufacturer. Each file represents a
discrete physical device type (e.g. make and model). These definitions can be loaded into NetBox instead of creating
new device type definitions manually.

If you would like to contribute to this library, please read through our [contributing guide](CONTRIBUTING.md) before
submitting content.

If you would like to automate the import of these devicetype template files, there is a **community based** python script
that will check for duplicates, allow you to selectively import vendors, etc. available here [minitriga/Netbox-Device-Type-Library-Import](https://github.com/minitriga/Netbox-Device-Type-Library-Import). **Note**: This is not related to NetBox in any official way and you will not get support for it here.

## Device Type Definitions

Each definition **must** include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this device type.
  - Type: String
- `model`: The model number of the device type. This must be unique per manufacturer.
  - Type: String
- `slug`: A URL-friendly representation of the model number. Like the model number, this must be unique per
  manufacturer.
  - Type: String
  - Pattern: `"^[-a-zA-Z0-9_]+$"`. Must match the following characters: `-`, `_`, Uppercase or Lowercase `a` to `z`, Numbers `0` to `9`.

The following fields may **optionally** be declared:

- `part_number`: An alternative representation of the model number (e.g. a SKU). (**Default: None**)
  - Type: String
- `u_height`: The height of the device type in rack units. Increments of 0.5U are supported. (**Default: 1**)
  - Type: number (minimum of `0`, multiple of `0.5`)
- `is_full_depth`: A boolean which indicates whether the device type consumes both the front and rear rack faces. (**Default: true**)
  - Type: Boolean
- `airflow`: A decleration of the airflow pattern for the device. (**Default: None**)
  - Type: String
  - Options:
    - `front-to-rear`
    - `rear-to-front`
    - `left-to-right`
    - `right-to-left`
    - `side-to-rear`
    - `passive`
- `subdevice_role`: Indicates that this is a `parent` or `child` device. (**Default: None**)
  - Type: String
  - Options:
    - `parent`
    - `child`
- `comments`: A string field which allows for comments to be added to the device. (**Default: None**)
  - Type: String

For further detail on these attributes and those listed below, please reference the
[schema definitions](schema/) and the [Component Definitions](#component-definitions) below.

### Component Definitions

Valid component types are listed below. Each type of component must declare a list of the individual component templates
to be added.

- [`console-ports`](#console-ports "Availible in NetBox 2 and later")
- [`console-server-ports`](#console-server-ports "Availible in NetBox 2.2 and later")
- [`power-ports`](#power-ports "Availible in NetBox 1.7 and later")
- [`power-outlets`](#power-outlets "Availible in NetBox 2 and later")
- [`interfaces`](#interfaces "Availible in all versions of NetBox")
- [`front-ports`](#front-ports "Availible in NetBox 2.5 and later")
- [`rear-ports`](#rear-ports "Availible in NetBox 2.5 and later")
- [`module-bays`](#module-bays "Availible in NetBox 3.2 and later")
- [`device-bays`](#device-bays "Availible in all versions of NetBox")
- [`inventory-items`](#inventory-items "Availible in NetBox 3.2 and later")

The available fields for each type of component are listed below.

#### Console Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)

#### Console Server Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)

#### Power Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)
- `maximum_draw`: The port's maximum power draw, in watts (optional)
- `allocated_draw`: The port's allocated power draw, in watts (optional)

#### Power Outlets

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)
- `power_port`: The name of the power port on the device which powers this outlet (optional)
- `feed_leg`: The phase (leg) of power to which this outlet is mapped; A, B, or C (optional)

#### Interfaces

- `name`: Name
- `label`: Label
- `type`: Interface type slug (API value)
- `mgmt_only`: A boolean which indicates whether this interface is used for management purposes only (default: false)

#### Front Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)
- `rear_port`: The name of the rear port on this device to which the front port maps
- `rear_port_position`: The corresponding position on the mapped rear port (default: 1)

#### Rear Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (API value)
- `positions`: The number of front ports that can map to this rear port (default: 1)

#### Module Bays

- `name`: Name
- `label`: Label
- `position`: The module bay's position within the parent device

#### Device Bays

- `name`: Name
- `label`: Label

#### Inventory Items

- `name`: Name
- `label`: Label
- `manufacturer`: The name of the manufacturer which produces this item
- `part_id`: The part ID assigned by the manufacturer

## Data Validation / Commit Quality Checks

There are two ways this repo focuses on keeping quality device-type definitions:

- **Pre-Commit Checks** - Optional, but **highly recommended**, for helping to identify simple issues before committing. (trailing-whitespace, end-of-file-fixer, check-yaml, yamlfmt, yamllint)
  - Installation
    - Virtual Environment Route
      - It is recommended to create a virtual env for your repo (`python3 -m venv venv`)
      - Install the required pip packages (`pip install -r requirements.txt`)
      - Continue to the "Install `pre-commit` Hooks"
    - `pre-commit` Only Route
      - [Install pre-commit](https://pre-commit.com/#install) (`pip install pre-commit`)
    - Install `pre-commit` Hooks
      - To install the pre-commit script: `pre-commit install`
  - Usage & Useful `pre-commit` Commands
    - After staging your files with `git`, to run the pre-commit script on changed files: `pre-commit run`
    - To run the pre-commit script on all files: `pre-commit run --all`
    - To uninstall the pre-commit script: `pre-commit uninstall`
  - Learn more about [pre-commit](https://pre-commit.com/)
- **GitHub Actions** - Automatically run before a PR can be merged. Repeats yamllint & validates against NetBox Device-Type Schema.
