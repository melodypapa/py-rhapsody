Working with Packages
======================

The ``package`` command provides operations for managing Rhapsody packages via CLI.

Synopsis
--------

::

   rhapsody-cli package <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple packages

delete
   Delete a package

view
   View package details

list
   List nested packages

update
   Update package attributes

package create
--------------

Create one or multiple packages with validated attributes.

**Usage:**

::

   rhapsody-cli package create [--path <parent-path>] [options] [attributes]

**Arguments:**

- ``--path <parent-path>`` - Parent package path (optional; defaults to project root when omitted)
- ``--input <json-file>`` - JSON file with package attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single package at project root::

   rhapsody-cli package create '{"name":"TopLevel","description":"Top-level package"}'

Create nested package under existing package::

   rhapsody-cli package create --path Sensors '{"name":"TempSensors","description":"Temperature sensors"}'

Create multiple packages at project root from file::

   rhapsody-cli package create --input packages.json

Create multiple packages nested under existing package::

   rhapsody-cli package create --path Sensors --input packages.json

Reuse exported package::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output package.json
   rhapsody-cli package create --path NewSensors package.json

**JSON Format:**

Single package::

   {
     "name": "TempSensors",
     "description": "Temperature sensors package",
     "stereotypes": ["auto_generated"],
     "tags": {"status": "active"}
   }

Multiple packages::

   [
     {"name": "TempSensors", "description": "Temperature"},
     {"name": "PressureSensors", "description": "Pressure"}
   ]

**Validated Attributes:**

- ``name`` (required) - Package name
- ``description`` - Plain text description
- ``description_html`` - HTML description
- ``properties`` - Custom properties object
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Tag name-value pairs

Unknown attributes are skipped with a warning log.

package delete
--------------

Delete a package and all its contents.

**Usage:**

::

   rhapsody-cli package delete --path <package-path>

**Example:**

::

   rhapsody-cli package delete --path Sensors/OldPackage

package view
------------

View package details in various formats.

**Usage:**

::

   rhapsody-cli package view --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Examples:**

View in table format::

   rhapsody-cli package view --path Sensors/TempSensors

Export to JSON file::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output package.json

Export to CSV::

   rhapsody-cli package view --path Sensors/TempSensors --format csv --output package.csv

**Output Formats:**

Table::

   +-----------+--------------------------------------+
   | Property  | Value                                |
   +-----------+--------------------------------------+
   | Name      | TempSensors                          |
   | GUID      | {12345678-1234-1234-1234-1234567890} |
   | Desc      | Temperature sensors package          |
   | MetaClass | Package                              |
   | FullPath  | Sensors/TempSensors                  |
   +-----------+--------------------------------------+

JSON::

   {
     "name": "TempSensors",
     "guid": "{12345678-1234-1234-1234-1234567890}",
     "description": "Temperature sensors package",
     "metaClass": "Package",
     "fullPath": "Sensors/TempSensors"
   }

CSV::

   Name,GUID,Description,MetaClass,FullPath
   TempSensors,{12345678-1234-1234-1234-1234567890},Temperature sensors package,Package,Sensors/TempSensors

package list
------------

List nested packages under a parent package.

**Usage:**

::

   rhapsody-cli package list --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Examples:**

List nested packages::

   rhapsody-cli package list --path Sensors

Export to JSON::

   rhapsody-cli package list --path Sensors --format json --output packages.json

**Output Formats:**

Table::

   +----------------+
   | Name           |
   +----------------+
   | TempSensors    |
   | PressureSensors|
   | FlowSensors    |
   +----------------+

JSON::

   ["TempSensors", "PressureSensors", "FlowSensors"]

CSV::

   Name
   TempSensors
   PressureSensors
   FlowSensors

package update
--------------

Update an existing package's attributes via path or GUID.

**Usage:**

::

   rhapsody-cli package update --path <package-path> [options] [attributes]
   rhapsody-cli package update --guid <guid> [options] [attributes]

**Arguments:**

- ``--path <package-path>`` - Package path to update (optional)
- ``--guid <guid>`` - Package GUID to update (optional)
- ``--input <json-file>`` - JSON file with package attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

Exactly one of ``--path`` or ``--guid`` must be specified.

**Examples:**

Update package name and description via path::

   rhapsody-cli package update --path Sensors/TempSensors '{"name":"NewName","description":"Updated description"}'

Update package via GUID::

   rhapsody-cli package update --guid 12345678-1234-1234-1234-123456789abc '{"description":"New description"}'

Update package from JSON file::

   rhapsody-cli package update --path Sensors/TempSensors --input update.json

**JSON Format:**

::

   {
     "name": "NewName",
     "description": "Updated description",
     "display_name": "Display Name",
     "stereotypes": ["auto_generated"],
     "tags": {"status": "active"},
     "properties": {"custom": "value"}
   }

**Validated Attributes:**

- ``name`` - Package name
- ``description`` - Plain text description
- ``display_name`` - Display name
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Tag name-value pairs
- ``properties`` - Custom properties object

.. note::

   Update performs a partial update: only the fields present in the JSON are
   modified. Fields omitted from the JSON are left unchanged. Unknown fields
   are skipped with a warning log.

   When using ``--guid``, the element type is validated. If the GUID does not
   resolve to a Package, a ``CliExecutionError`` is raised.

Workflow: Package Cloning
-------------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export package to JSON::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output template.json

**Step 2:** Edit template.json (modify name, description, etc.)

**Step 3:** Create new package from template::

   rhapsody-cli package create --path NewSensors template.json

Error Handling
--------------

All commands validate the path before execution:

- Path must exist in the model
- Path must resolve to a Package element (not Class, Actor, etc.)
- Invalid path raises ``CliExecutionError``

Examples of errors::

   Path 'Sensors/Invalid' not found
   Path 'Sensors/MyClass' does not resolve to a Package (found Class)

See Also
--------

- :doc:`working_with_elements` - Generic element operations
- :doc:`working_with_projects` - Project management operations
