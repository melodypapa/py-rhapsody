Working with Classes
====================

The ``class`` command provides operations for managing Rhapsody class elements
via CLI. It mirrors the ``package`` command structure and adds support for
class-specific features like boolean flags, operations, attributes, and
generalization relationships.

Synopsis
--------

::

   rhapsody-cli class <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple classes

delete
   Delete a class

view
   View class details

list
   List classes in a package

link
   Add or remove generalization relationships

update
   Update class attributes

class create
------------

Create one or multiple classes with validated attributes.

**Usage:**

::

   rhapsody-cli class create --path <parent-package-path> [options] [attributes]

**Arguments:**

- ``--path <parent-package-path>`` - Parent package path (required). Accepts
  package or project root.
- ``--input <json-file>`` - JSON file with class attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single class with inline JSON::

   rhapsody-cli class create --path Sensors '{"name":"TemperatureSensor","description":"Temp sensor"}'

Create multiple classes from file::

   rhapsody-cli class create --path Sensors --input classes.json

**JSON Format (single class):**

::

   {
     "name": "TemperatureSensor",
     "description": "Temperature sensor class",
     "isAbstract": false,
     "isFinal": false,
     "isActive": false,
     "stereotypes": ["active"],
     "tags": {"status": "active"},
     "operations": ["readValue", "setThreshold"],
     "attributes": ["threshold", "unit"],
     "superclasses": ["BaseSensor"]
   }

**Validated Attributes:**

- ``name`` (required) - Class name
- ``description`` - Plain text description
- ``isAbstract`` - Boolean, sets via setIsAbstract(1/0)
- ``isFinal`` - Boolean, sets via setIsFinal(1/0)
- ``isActive`` - Boolean, sets via setIsActive(1/0)
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Object of key-value pairs
- ``operations`` - Array of operation names
- ``attributes`` - Array of attribute names
- ``superclasses`` - Array of superclass names (resolved via findNestedClassifierRecursive)

class delete
------------

Delete a class by path or GUID.

**Usage:**

::

   rhapsody-cli class delete --path <class-path>
   rhapsody-cli class delete --guid <guid>

**Arguments:**

- ``--path <class-path>`` - Class path to delete (optional)
- ``--guid <guid>`` - Class GUID to delete (format: 12345678-1234-1234-1234-123456789abc)

Exactly one of ``--path`` or ``--guid`` must be specified.

**Example:**

::

   rhapsody-cli class delete --path Sensors/OldClass
   rhapsody-cli class delete --guid 12345678-1234-1234-1234-123456789abc

class view
----------

View class details in various formats.

**Usage:**

::

   rhapsody-cli class view --path <class-path> [options]
   rhapsody-cli class view --guid <guid> [options]

**Arguments:**

- ``--path <class-path>`` - Class path to view (optional)
- ``--guid <guid>`` - Class GUID to view (optional)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

Exactly one of ``--path`` or ``--guid`` must be specified.

**View Fields:**

Name, GUID, Description, IsAbstract, IsActive, IsFinal, IsComposite,
IsReactive, MetaClass, FullPath, Operations, Attributes

**Output Formats:**

Table (default)::

   Property     | Value
   -------------|---------------------
   Name         | TemperatureSensor
   GUID         | 12345678-...
   IsAbstract   | 0
   Operations   | readValue, setThreshold
   Attributes   | threshold, unit

JSON::

   {
     "name": "TemperatureSensor",
     "guid": "12345678-...",
     "isAbstract": 0,
     "operations": ["readValue", "setThreshold"],
     "attributes": ["threshold", "unit"]
   }

CSV (horizontal)::

   Name,GUID,Description,IsAbstract,...,Operations,Attributes
   TemperatureSensor,12345678-...,Temp sensor,0,...,"readValue,setThreshold","threshold,unit"

class list
----------

List classes in a package.

**Usage:**

::

   rhapsody-cli class list --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required). Accepts package or project root.
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Output Formats:**

Table::

   +--------------------+
   | Name               |
   +--------------------+
   | TemperatureSensor  |
   | PressureSensor     |
   +--------------------+

JSON::

   ["TemperatureSensor", "PressureSensor"]

CSV::

   Name
   TemperatureSensor
   PressureSensor

class link
----------

Add or remove generalization relationships between classes.

**Usage:**

::

   rhapsody-cli class link --path <class-path> --add <target-name>
   rhapsody-cli class link --path <class-path> --remove <target-name>
   rhapsody-cli class link --guid <guid> --add <target-name>

**Arguments:**

- ``--path <class-path>`` - Source class path (optional)
- ``--guid <guid>`` - Source class GUID (optional)
- ``--add <class-name>`` - Add a generalization to target class by name
- ``--remove <class-name>`` - Remove a generalization to target class by name
- ``--type <generalization>`` - Relationship type (default: generalization;
  v1 supports only generalization)

Exactly one of ``--path`` or ``--guid`` must be specified. Exactly one of
``--add`` or ``--remove`` must be specified.

**Examples:**

::

   # Add generalization
   rhapsody-cli class link --path Sensors/TemperatureSensor --add BaseSensor

   # Remove generalization
   rhapsody-cli class link --path Sensors/TemperatureSensor --remove BaseSensor

   # Using GUID
   rhapsody-cli class link --guid 12345678-1234-1234-1234-123456789abc --add BaseSensor

class update
------------

Update an existing class's attributes via path or GUID.

**Usage:**

::

   rhapsody-cli class update --path <class-path> [options] [attributes]
   rhapsody-cli class update --guid <guid> [options] [attributes]

**Arguments:**

- ``--path <class-path>`` - Class path to update (optional)
- ``--guid <guid>`` - Class GUID to update (optional)
- ``--input <json-file>`` - JSON file with class attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

Exactly one of ``--path`` or ``--guid`` must be specified.

**Examples:**

Update class name and description via path::

   rhapsody-cli class update --path Sensors/TemperatureSensor '{"name":"NewName","description":"Updated"}'

Update class boolean flags via path::

   rhapsody-cli class update --path Sensors/TemperatureSensor '{"isAbstract":true,"isActive":true}'

Update class via GUID::

   rhapsody-cli class update --guid 12345678-1234-1234-1234-123456789abc '{"description":"New description"}'

**JSON Format:**

::

   {
     "name": "NewName",
     "description": "Updated description",
     "isAbstract": true,
     "isFinal": false,
     "isActive": true,
     "stereotypes": ["active"],
     "tags": {"status": "active"}
   }

**Validated Attributes:**

- ``name`` - Class name
- ``description`` - Plain text description
- ``isAbstract`` - Boolean, sets via setIsAbstract(1/0)
- ``isFinal`` - Boolean, sets via setIsFinal(1/0)
- ``isActive`` - Boolean, sets via setIsActive(1/0)
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Object of key-value pairs

.. note::

   Update performs a partial update: only the fields present in the JSON are
   modified. Fields omitted from the JSON are left unchanged. Unknown fields
   are skipped with a warning log.

   Operations, attributes, and superclasses are not managed via ``update``.
   Use the dedicated ``class create`` (with operations/attributes/superclasses
   arrays) and ``class link`` (for generalization relationships) commands
   instead.

   When using ``--guid``, the element type is validated. If the GUID does not
   resolve to a Class, a ``CliExecutionError`` is raised.

Workflow: Class Cloning
-----------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export class to JSON::

   rhapsody-cli class view --path Sensors/TemperatureSensor --format json --output template.json

**Step 2:** Edit template.json (modify name, description, etc.)

**Step 3:** Create new class from template::

   rhapsody-cli class create --path NewSensors template.json

Unknown fields (``guid``, ``isComposite``, ``isReactive``, ``metaClass``,
``fullPath``) are skipped during create with a warning. All other fields
round-trip cleanly.

Error Handling
--------------

All commands validate the path before execution:

- Path must exist in the model
- Path must resolve to the expected element type (Package/Project for create/list;
  Class for delete/view/link)
- Invalid path raises ``CliExecutionError``

See Also
--------

- :doc:`working_with_packages` - Package management operations
- :doc:`working_with_elements` - Generic element operations