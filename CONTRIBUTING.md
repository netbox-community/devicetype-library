# Contributing

This library is maintained by and for the community of NetBox users. As such, the regular contribution of accurate and
complete device type definitions is crucial to its success.

## Writing Definition Files

Each NetBox device type definition exists as a single YAML file, arranged by manufacturer (vendor). Files are named by
concatenating the definition's model name with a `.yaml` extension. For example:

```no-highlight
device-types/Acme/BFR-1000.yaml
device-types/Acme/BFR-2000.yaml
```

When writing new definitions, there are some important guidelines to follow:

* Every unique model number requires a discrete definition file, even if the set of components is identical.
* Definition files must end in `.yaml`, or `.yml`
* Use proper, human-friendly names when creating manufacturer directories (e.g. `Alcatel-Lucent` versus `alcatel`).
* Include only components which are fixed to the chassis. Optional modular components should be omitted from the
  definition. (Note that this does not exclude field-replaceable hardware that is expected to always be present, such
  as power supplies.)
* Name components exactly as they appear in the device's operating system (as opposed to the physical chassis label, if
  different).
* Use the complete form of interface names where applicable. For example, use `TenGigabitEthernet1/2/3` instead of
`Te1/2/3`.

Additionally, be sure to adhere to the following style guidance:

* Do not begin the file with three dashes (`---`); YAML directives are not supported.
* Use two spaces for indenting.
* Specify a device type's attributes before listing its components.
* Avoid encapsulating YAML values in quotes unless necessary to avoid a syntax error.

## The Contribution Workflow

The process of submitting new definitions to the library is as follows:

1. Verify that the proposed definition does not duplicate or conflict with an existing definition. (If unsure, please
   raise an issue seeking clarification prior to submitting a PR.)
2. [Fork](https://guides.github.com/activities/forking/) the GitHub project and create a new branch to hold your
   proposed changes. If adding new definitions, the branch should be named so that it loosely follows the format `<manufacturer>-<series>` (for example, `cisco-c9300`).
3. Introduce the new content exactly as it should appear once accepted.
4. Submit a [pull request](https://github.com/netbox-community/devicetype-library/compare?expand=1) to merge your new
   branch into the `master` branch. Include a brief description of the changes introduced in the PR.
5. GitHub will automatically run tests against your PR to validate it. If the tests fail, make the necessary changes to
   your branch so that they pass (or rescind the PR until you are able to do so). Please note that PRs which do not pass
   validation will be closed.
5. A maintainer will review your PR and take one of three actions:
   * Accept and merge it
   * Request revisions
   * Close the PR citing a reason (e.g. failing validation or not applicable to the library)
