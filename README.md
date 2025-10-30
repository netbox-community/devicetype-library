# NetBox Device Type Library

## About this Library

This library is intended to be used for populating device types in [NetBox](https://github.com/netbox-community/netbox).
It contains a set of device type definitions expressed in YAML and arranged by manufacturer. Each file represents a
discrete physical device type (e.g. make and model). These definitions can be loaded into NetBox instead of creating
new device type definitions manually.

If you would like to contribute to this library, please read through our [contributing guide](CONTRIBUTING.md) before
submitting content.

If you would like to automate the import of these devicetype template files, there is a NetBox Community python script
that will check for duplicates, allow you to selectively import vendors, etc. available here [netbox-community/Device-Type-Library-Import](https://github.com/netbox-community/Device-Type-Library-Import).

## Device Type Definitions

Each definition **must** include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this device type.
  - Type: String
- `model`: The model number of the device type. This must be unique per manufacturer.
  - Type: String
- `slug`: A URL-friendly representation of the model number. Like the model number, this must be unique per
  manufacturer. All slugs should have the manufacturers name prepended to it with a dash, please see the example below.
  - Type: String
  - Pattern: `"^[-a-z0-9_]+$"`. Must match the following characters: `-`, Lowercase `a` to `z`, Numbers `0` to `9`.
- `u_height`: The height of the device type in rack units. Increments of 0.5U are supported. (**Note: For Child devices u_height must be 0**)
  - Type: number (minimum of `0`, multiple of `0.5`
  - :test_tube: Example: `u_height: 12.5`
- `is_full_depth`: A boolean which indicates whether the device type consumes both the front and rear rack faces. (**Default: true**)
  - Type: Boolean
  - :test_tube: Example: `is_full_depth: false`

:test_tube: Example:

  ```yaml
  manufacturer: Dell
  model: PowerEdge R670
  slug: dell-poweredge-r670
  u_height: 1
  is_full_depth: true
  ```

**Note: We are asking that all new deivces also include the following optional fields: `airflow`, `weight` and `weight_unit`.**

The following fields may **optionally** be declared:

- `part_number`: An alternative representation of the model number (e.g. a SKU). (**Default: None**)
  - Type: String
  - :test_tube: Example: `part_number: D109-C3`
- `airflow`: A declaration of the airflow pattern for the device. (**Default: None**)
  - Type: String
  - Options:
    - `front-to-rear`
    - `rear-to-front`
    - `left-to-right`
    - `right-to-left`
    - `side-to-rear`
    - `rear-to-side`
    - `bottom-to-top`
    - `top-to-bottom`
    - `passive`
    - `mixed`
  - :test_tube: Example: `airflow: side-to-rear`
- `front_image`: Indicates that this device has a front elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <VALUE_IN_SLUG>.front.<acceptable_format>
  - Type: Boolean
  - :test_tube: Example: `front_image: true`
- `rear_image`: Indicates that this device has a rear elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <VALUE_IN_SLUG>.rear.<acceptable_format>
  - Type: Boolean
  - :test_tube: Example: `rear_image: true`
- `subdevice_role`: Indicates that this is a `parent` or `child` device. (**Default: None**)
  - Type: String
  - Options:
    - `parent`
    - `child`
  - :test_tube: Example: `subdevice_role: parent`
- `comments`: A string field which allows for comments to be added to the device. (**Default: None**)
  - Type: String
  - :test_tube: Example: `comments: This is a comment that will appear on all NetBox devices of this type`
- `is_powered`: A boolean which indicates whether the device type does not take power. This is mainly used as a workaround for validation testing on non powered devices (i.e. rackmount kits or patch pannels.) (**Default: True**)
  - Type: Boolean
  - :test_tube: Example: `is_powered: false`
- `weight`: A number representing the numeric weight value. Must be a multiple of 0.01 (2 decimal places). (**Default: None**)
  - Type: Number
  - Value: must be a multiple of 0.01
- `weight_unit`: A string defining the unit of measurement. It must be one of the supported values. (**Default: None**)
  - Type: String
  - Options:
    - `kg`
    - `g`
    - `lb`
    - `oz`
  - :test_tube: Example:

    ```yaml
    weight: 12.21
    weight_unit: lb
    ```

For further detail on these attributes and those listed below, please reference the
[schema definitions](schema/) and the [Component Definitions](#component-definitions) below.

## Rack Type Definitions

Each definition **must** include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this rack type.
  - Type: String
- `model`: The model number of the rack type. This must be unique per manufacturer.
  - Type: String
- `slug`: A URL-friendly representation of the model number. Like the model number, this must be unique per
  manufacturer. All slugs should have the manufacturers name prepended to it with a dash, please see the example below.
  - Type: String
  - Pattern: `"^[-a-z0-9_]+$"`. Must match the following characters: `-`, Lowercase `a` to `z`, Numbers `0` to `9`.
- `form_factor`: The form factor of the rack type. This is used to indicate the physical characteristics of the rack, such as whether it is a 4-post frame or a wall-cabinet etc.
  - Type: String
  - :test_tube: Example: `form_factor: 4-post-frame`
- `width`: The width of the rack type in zoll/inches. This is used to indicate the physical width of the rack, such as whether it is a 19" or 23" rack.
  - Type: Integer
  - :test_tube: Example: `width: 19`
- `u_height`: The height of the rack type in rack units.
  - Type: Number
  - :test_tube: Example: `u_height: 42`
- `starting_unit`: The unit number at which the rack starts. This is used to indicate the starting unit number of the rack, such as whether it starts at 1 or 42. The starting unit is normally defined from bottom to top, with the bottom unit being 1.
  - Type: Number
  - :test_tube: Example: `starting_unit: 1`

:test_tube: Example:

  ```yaml
  manufacturer: Startech
  model: 4 Post 42U
  slug: startech-4postrack42
  form_factor: 4-post-frame
  width: 19
  u_height: 42
  starting_unit: 1
  ```

**Note: We are asking that all new racks also include the following optional fields: `outer_width`, `outer_height`, `outer_depth`, `outer_unit`, `weight`, `max_weight`, `weight_unit`, `mounting_depth`, and `desc_units`.**

For further detail on these attributes and those listed below, please reference the
[racktype schema definition](schema/racktype.json)

### Component Definitions

Valid component types are listed below. Each type of component must declare a list of the individual component templates
to be added.

- [console-ports](#console-ports "Availible in NetBox 2 and later")
- [console-server-ports](#console-server-ports "Availible in NetBox 2.2 and later")
- [power-ports](#power-ports "Availible in NetBox 1.7 and later")
- [power-outlets](#power-outlets "Availible in NetBox 2 and later")
- [interfaces](#interfaces "Availible in all versions of NetBox")
- [front-ports](#front-ports "Availible in NetBox 2.5 and later")
- [rear-ports](#rear-ports "Availible in NetBox 2.5 and later")
- [module-bays](#module-bays "Availible in NetBox 3.2 and later")
- [device-bays](#device-bays "Availible in all versions of NetBox")
- [inventory-items](#inventory-items "Availible in NetBox 3.2 and later")

The available fields for each type of component are listed below.

#### Console Ports

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/consoleport/)**

A console port provides connectivity to the physical console of a device. These are typically used for temporary access by someone who is physically near the device, or for remote out-of-band access provided via a networked console server.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `_is_power_source`: Indicates that the port provides power to the device, only used internally for power validation (default: false)

#### Console Server Ports

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/consoleserverport/)**

A console server is a device which provides remote access to the local consoles of connected devices. They are typically used to provide remote out-of-band access to network devices, and generally connect to console ports.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)

#### Power Ports

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/powerport/)**

A power port is a device component which draws power from some external source (e.g. an upstream power outlet), and generally represents a power supply internal to a device.
**Note: Devices that have removeable Power Supplies, Like FRUs, should be modeled in the device as `module-bays` and then the PSU module should have the required `power-port`**

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `maximum_draw`: The port's maximum power draw, in watts (optional)
- `allocated_draw`: The port's allocated power draw, in watts (optional)

#### Power Outlets

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/poweroutlet/)**

Power outlets represent the outlets on a power distribution unit (PDU) or other device that supplies power to dependent devices. Each power port may be assigned a physical type, and may be associated with a specific feed leg (where three-phase power is used) and/or a specific upstream power port. This association can be used to model the distribution of power within a device.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `power_port`: The name of the power port on the device which powers this outlet (optional)
- `feed_leg`: The phase (leg) of power to which this outlet is mapped; A, B, or C (optional)

#### Interfaces

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/interface/)**

Interfaces in NetBox represent network interfaces used to exchange data with connected devices. On modern networks, these are most commonly Ethernet, but other types are supported as well. IP addresses and VLANs can be assigned to interfaces.

- `name`: Name
- `label`: Label
- `type`: Interface type slug (Array)
- `mgmt_only`: A boolean which indicates whether this interface is used for management purposes only (default: false)
- `poe_mode` : For if a device is POE powered (pd) or provides POE (pse)
- `poe_type` : The classification of PoE transmission supported, for PoE-enabled interfaces.

#### Front Ports

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/frontport/)**

Front ports are pass-through ports which represent physical cable connections that comprise part of a longer path. For example, the ports on the front face of a UTP patch panel would be modeled in NetBox as front ports. Each port is assigned a physical type, and must be mapped to a specific rear port on the same device. A single rear port may be mapped to multiple front ports, using numeric positions to annotate the specific alignment of each.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `rear_port`: The name of the rear port on this device to which the front port maps
- `rear_port_position`: The corresponding position on the mapped rear port (default: 1)

#### Rear Ports

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/rearport/)**

Like front ports, rear ports are pass-through ports which represent the continuation of a path from one cable to the next. Each rear port is defined with its physical type and a number of positions: Rear ports with more than one position can be mapped to multiple front ports. This can be useful for modeling instances where multiple paths share a common cable (for example, six discrete two-strand fiber connections sharing a 12-strand MPO cable).

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `positions`: The number of front ports that can map to this rear port (default: 1)
- `_is_power_source`: Indicates that the port provides power to the device, only used internally for power validation (default: false)

#### Module Bays

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/modulebay/)**

Module bays represent a space or slot within a device in which a field-replaceable module may be installed. A common example is that of a chassis-based switch such as the Cisco Nexus 9000 or Juniper EX9200. Modules in turn hold additional components that become available to the parent device.
**Note: Field Replacable Power Supply’s should also be modeled as module bays**

- `name`: Name
- `label`: Label
- `position`: The alphanumeric position in which this module bay is situated within the parent device. When creating module components, the string `{module}` in the component name will be replaced with the module bay's `position`. See the [NetBox Documentation](https://docs.netbox.dev/en/stable/models/dcim/moduletype/#automatic-component-renaming) for more details.

#### Device Bays

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/devicebay/)**

Device bays represent a space or slot within a parent device in which a child device may be installed. For example, a 2U parent chassis might house four individual blade servers. The chassis would appear in the rack elevation as a 2U device with four device bays, and each server within it would be defined as a 0U device installed in one of the device bays. Child devices do not appear within rack elevations or count as consuming rack units.

Child devices are first-class Devices in their own right: That is, they are fully independent managed entities which don't share any control plane with the parent. Just like normal devices, child devices have their own platform (OS), role, tags, and components. LAG interfaces may not group interfaces belonging to different child devices.

- `name`: Name
- `label`: Label

#### Inventory Items

**[Documentation](https://docs.netbox.dev/en/stable/models/dcim/inventoryitem/)**

Inventory items represent hardware components installed within a device, such as a power supply or CPU or line card. They are intended to be used primarily for inventory purposes.

Inventory items are hierarchical in nature, such that any individual item may be designated as the parent for other items. For example, an inventory item might be created to represent a line card which houses several SFP optics, each of which exists as a child item within the device. An inventory item may also be associated with a specific component within the same device. For example, you may wish to associate a transceiver with an interface.

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
    - To run the pre-commit script on all files: `pre-commit run -a`
    - To uninstall the pre-commit script: `pre-commit uninstall`
  - Learn more about [pre-commit](https://pre-commit.com/)
- **GitHub Actions** - Automatically run before a PR can be merged. Repeats yamllint & validates against NetBox Device-Type Schema.
