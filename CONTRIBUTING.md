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

- Every unique model number requires a discrete definition file, even if the set of components is identical.
- Definition files must end in `.yaml`, or `.yml`
- Use proper, human-friendly names when creating manufacturer directories (e.g. `Alcatel-Lucent` versus `alcatel`).
- Include only components which are fixed to the chassis. Module bays and associated module types should be included for
  all modular components which can be modelled in NetBox (network modules, power supplies, etc).
- Name components exactly as they appear in the device's operating system (as opposed to the physical chassis label, if
  different).
- Use the complete form of interface names where applicable. For example, use `TenGigabitEthernet1/2/3` instead of
`Te1/2/3`.

Additionally, be sure to adhere to the following style guidance:

- Use two spaces for indenting.
- Specify a device type's attributes before listing its components.
- Avoid encapsulating YAML values in quotes unless necessary to avoid a syntax error.
- End each definition file with a blank line.

## The Contribution Workflow

The process of submitting new definitions to the library is as follows:

1. Verify that the proposed definition does not duplicate or conflict with an existing definition. (If unsure, please
   raise an issue seeking clarification prior to submitting a PR.)
1. [Fork](https://guides.github.com/activities/forking/) the GitHub project and create a new branch to hold your
   proposed changes. If adding new definitions, the branch should be named so that it loosely follows the format `<manufacturer>-<series>` (for example, `cisco-c9300`).
1. Install & run included pre-commit script as described in the [README.md](README.md) (Optional, but recommended)
1. Introduce the new content exactly as it should appear once accepted.
1. Create a [draft pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests#draft-pull-requests) to merge your new branch into the `master` branch. Include a brief description of the changes introduced in the PR.
1. GitHub will automatically run tests against your draft PR to validate it. If the tests fail, make the necessary changes to
   your branch so that they pass.
1. Submit the [pull request](https://github.com/netbox-community/devicetype-library/compare?expand=1) for review. Please note that submitted PRs
   which do not pass validation will be closed and must be rescinded.
1. A maintainer will review your PR and take one of three actions:
   - Approve and merge it
   - Request revisions
   - Close the PR citing a reason (e.g. failing validation or not applicable to the library)
