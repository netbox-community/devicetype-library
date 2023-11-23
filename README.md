# NetBox Device Type Library

## About this Library

This library is intended to be used for populating device types in [NetBox](https://github.com/netbox-community/netbox).
It contains a set of device type definitions expressed in YAML and arranged by manufacturer. Each file represents a
discrete physical device type (e.g. make and model). These definitions can be loaded into NetBox instead of creating
new device type definitions manually.

If you would like to contribute to this library, please read through our [contributing guide](CONTRIBUTING.md) before
submitting content.

**Note: As of March 2023 Netbox-Device-Type-Library-Import has been brought into the NetBox Community Organization. We will work to get this fully supported soon.**
If you would like to automate the import of these devicetype template files, there is a NetBox Community ~~**community based**~~ python script
that will check for duplicates, allow you to selectively import vendors, etc. available here [netbox-community/Device-Type-Library-Import](https://github.com/netbox-community/Device-Type-Library-Import). ~~**Note**: This is not related to NetBox in any official way and you will not get support for it here.~~

## Device Type Definitions

Each definition **must** include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this device type.
  - Type: String
- `model`: The model number of the device type. This must be unique per manufacturer.
  - Type: String
- `slug`: A URL-friendly representation of the model number. Like the model number, this must be unique per
  manufacturer. All slugs should have the manufacturers name prepended to it with a dash, please see the example below.
  - Type: String
  - Pattern: `"^[-a-zA-Z0-9_]+$"`. Must match the following characters: `-`, `_`, Uppercase or Lowercase `a` to `z`, Numbers `0` to `9`.

>:test_tube: **Valid Example**:
>```
>manufacturer: Dell
>model: PowerEdge R6515
>slug: dell-poweredge-r6515
>```

The following fields may **optionally** be declared:

- `part_number`: An alternative representation of the model number (e.g. a SKU). (**Default: None**)
  - Type: String
> :test_tube: **Example**: `part_number: D109-C3`
- `u_height`: The height of the device type in rack units. Increments of 0.5U are supported. (**Default: 1**)
  - Type: number (minimum of `0`, multiple of `0.5`)
> :test_tube: **Example**: `u_height: 12.5`
- `is_full_depth`: A boolean which indicates whether the device type consumes both the front and rear rack faces. (**Default: true**)
  - Type: Boolean
> :test_tube: **Example**: `is_full_depth: false`
- `airflow`: A declaration of the airflow pattern for the device. (**Default: None**)
  - Type: String
  - Options:
    - `front-to-rear`
    - `rear-to-front`
    - `left-to-right`
    - `right-to-left`
    - `side-to-rear`
    - `passive`
> :test_tube: **Example**: `airflow: side-to-rear`
- `front_image`: Indicates that this device has a front elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <VALUE_IN_SLUG>.front.<acceptable_format>
  - Type: Boolean
> :test_tube: **Example**: `front_image: True`
- `rear_image`: Indicates that this device has a rear elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <VALUE_IN_SLUG>.rear.<acceptable_format>
  - Type: Boolean
> :test_tube: **Example**: `rear_image: True`
- `subdevice_role`: Indicates that this is a `parent` or `child` device. (**Default: None**)
  - Type: String
  - Options:
    - `parent`
    - `child`
> :test_tube: **Example**: `subdevice_role: parent`
- `comments`: A string field which allows for comments to be added to the device. (**Default: None**)
  - Type: String
> :test_tube: **Example**: `comments: This is a comment that will appear on all NetBox devices of this type`
- `weight`: A number representing the numeric weight value. Must be a multiple of 0.01 (2 decimal places). (**Default: None**)
    - Type: Number
    - Value: must be a multiple of 0.01
- `weight_unit`: A string defining the unit of measurement. It must be one of the supported values. (**Default: None**)
  - Type: String
  - Value: Enumerated Options
    - kg
    - g
    - lb
    - oz
>:test_tube: **Example**:
>```
>weight: 12.21
>weight_unit: lb
>```
- `is_powered`: A boolean which indicates whether the device type does not take power. This is mainly used as a workaround for validation testing on non-devices (i.e. rackmount kits for mounting desktop devices) (**Default: True**)
  - Type: Boolean
> :test_tube: **Example**: `is_powered: false`

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
- `type`: Port type slug (Array)
- `poe`: Does this port access/provide POE? (Boolean)

#### Console Server Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)

#### Power Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `maximum_draw`: The port's maximum power draw, in watts (optional)
- `allocated_draw`: The port's allocated power draw, in watts (optional)

#### Power Outlets

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `power_port`: The name of the power port on the device which powers this outlet (optional)
- `feed_leg`: The phase (leg) of power to which this outlet is mapped; A, B, or C (optional)

#### Interfaces

- `name`: Name
- `label`: Label
- `type`: Interface type slug (Array)
- `mgmt_only`: A boolean which indicates whether this interface is used for management purposes only (default: false)

#### Front Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `rear_port`: The name of the rear port on this device to which the front port maps
- `rear_port_position`: The corresponding position on the mapped rear port (default: 1)

#### Rear Ports

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `positions`: The number of front ports that can map to this rear port (default: 1)
- `poe`: Does this port access/provide POE? (Boolean)

#### Module Bays

- `name`: Name
- `label`: Label
- `position`: The alphanumeric position in which this module bay is situated within the parent device. When creating module components, the string `{module}` in the component name will be replaced with the module bay's `position`. See the [NetBox Documentation](https://docs.netbox.dev/en/stable/models/dcim/moduletype/#automatic-component-renaming) for more details.

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
