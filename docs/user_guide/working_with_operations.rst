Working with Operations
=======================

The ``operation`` command provides operations for managing Rhapsody operation
elements via CLI. Operations are behavioral features of classifiers (classes
and interfaces) and define the methods that the classifier can perform. The
command mirrors the ``class`` command structure and adds support for
operation-specific features like ``returns`` type resolution, boolean flags
(``isAbstract``, ``isStatic``, ``isVirtual``), and ``arguments``.

Synopsis
--------

::

   rhapsody-cli operation <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple operations

delete
   Delete an operation

view
   View operation details

list
   List operations on a classifier

update
   Modify attributes of an existing operation

operation create
----------------

Create one or multiple operations with validated attributes.

**Usage:**

::

   rhapsody-cli operation create --path <parent-classifier-path> [options] [attributes]

**Arguments:**

- ``--path <parent-classifier-path>`` - Parent classifier path (required).
  Must resolve to a Classifier element (Class, Interface, etc.).
- ``--input <json-file>`` - JSON file with operation attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single operation with inline JSON::

   rhapsody-cli operation create --path Sensors/TemperatureSensor '{"name":"readValue","body":"return value;"}'

Create multiple operations from file::

   rhapsody-cli operation create --path Sensors/TemperatureSensor --input operations.json

**JSON Format (single operation):**

::

   {
     "name": "readValue",
     "body": "return this.value;",
     "isAbstract": false,
     "isStatic": false,
     "isVirtual": true,
     "returns": "double",
     "visibility": "public",
     "arguments": "double threshold",
     "description": "Reads the current sensor value"
   }

**Validated Attributes:**

- ``name`` (required) - Operation name, applied via ``addOperation()``
- ``body`` - Operation body (implementation), applied via ``setBody()``
- ``isAbstract`` - Boolean, sets via ``setIsAbstract(1/0)``
- ``isStatic`` - Boolean, sets via ``setIsStatic(1/0)``
- ``isVirtual`` - Boolean, sets via ``setIsVirtual(1/0)``
- ``returns`` - Return type name, resolved via
  ``findNestedClassifierRecursive()`` on the parent classifier's package
- ``visibility`` - Visibility string (e.g. ``public``, ``private``),
  applied via ``setVisibility()``
- ``arguments`` - Arguments string, applied via ``setArguments()``
- ``description`` - Plain text description, applied via ``setDescription()``

Unknown fields are skipped with a warning log.

operation delete
----------------

Delete an operation by path + name, or by GUID.

**Usage:**

::

   rhapsody-cli operation delete --path <class-path> --name <operation-name>
   rhapsody-cli operation delete --guid <guid>

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <operation-name>`` - Operation name within class (optional)
- ``--guid <guid>`` - Operation GUID to delete
  (format: 12345678-1234-1234-1234-123456789abc)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Operation``; a mismatch raises ``CliExecutionError``.

**Example:**

::

   rhapsody-cli operation delete --path Sensors/TemperatureSensor --name readValue
   rhapsody-cli operation delete --guid 12345678-1234-1234-1234-123456789abc

operation view
--------------

View operation details in various formats.

**Usage:**

::

   rhapsody-cli operation view --path <class-path> --name <operation-name> [options]
   rhapsody-cli operation view --guid <guid> [options]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <operation-name>`` - Operation name within class (optional)
- ``--guid <guid>`` - Operation GUID to view (optional)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified.

**View Fields (12):**

Name, GUID, Description, Body, IsAbstract, IsStatic, IsVirtual, Returns,
Visibility, Arguments, MetaClass, FullPath

**Output Formats:**

Table (default)::

   Property     | Value
   -------------|---------------------
   Name         | readValue
   GUID         | 12345678-...
   IsAbstract   | 0
   IsVirtual    | 1
   Returns      | double
   Visibility   | public
   Arguments    | double threshold

JSON::

   {
     "name": "readValue",
     "guid": "12345678-...",
     "isAbstract": 0,
     "isStatic": 0,
     "isVirtual": 1,
     "returns": "double",
     "visibility": "public",
     "arguments": "double threshold"
   }

CSV (horizontal)::

   Name,GUID,Description,Body,IsAbstract,IsStatic,IsVirtual,Returns,Visibility,Arguments,MetaClass,FullPath
   readValue,12345678-...,Reads value,...,0,0,1,double,public,double threshold,Operation,Sensors/TemperatureSensor/readValue

operation list
--------------

List operations on a classifier.

**Usage:**

::

   rhapsody-cli operation list --path <class-path> [options]

**Arguments:**

- ``--path <class-path>`` - Classifier path (required). Accepts a classifier
  element (Class, Interface, etc.).
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Output Formats:**

Table::

   +--------------------+
   | Name               |
   +--------------------+
   | readValue          |
   | setThreshold       |
   +--------------------+

JSON::

   ["readValue", "setThreshold"]

CSV::

   Name
   readValue
   setThreshold

operation update
----------------

Modify attributes of an existing operation. Only specified fields are
modified (partial update).

**Usage:**

::

   rhapsody-cli operation update --path <class-path> --name <operation-name> [options] [attributes]
   rhapsody-cli operation update --guid <guid> [options] [attributes]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <operation-name>`` - Operation name within class (optional)
- ``--guid <guid>`` - Operation GUID to update (optional)
- ``--input <json-file>`` - JSON file with fields to update (optional)
- ``attributes`` - Inline JSON with fields to update (required if --input not
  specified)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Operation``.

**Examples:**

Update body only::

   rhapsody-cli operation update --path Sensors/TemperatureSensor --name readValue '{"body":"return value + offset;"}'

Update visibility and arguments::

   rhapsody-cli operation update --path Sensors/TemperatureSensor --name readValue '{"visibility":"protected","arguments":"int mode"}'

Update by GUID::

   rhapsody-cli operation update --guid 12345678-1234-1234-1234-123456789abc '{"body":"// TODO"}'

**Updatable Attributes:**

The same validated attributes as ``create``: ``name``, ``body``,
``isAbstract``, ``isStatic``, ``isVirtual``, ``returns``, ``visibility``,
``arguments``, ``description``. Unknown fields are skipped with a warning.

Workflow: Operation Cloning
---------------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export operation to JSON::

   rhapsody-cli operation view --path Sensors/TemperatureSensor --name readValue --format json --output template.json

**Step 2:** Edit template.json (modify name, body, etc.)

**Step 3:** Create new operation from template::

   rhapsody-cli operation create --path Sensors/PressureSensor template.json

Unknown fields (``guid``, ``metaClass``, ``fullPath``) are skipped during
create with a warning. All other fields round-trip cleanly.

Error Handling
--------------

All commands validate inputs before execution:

- ``--path`` must resolve to an existing element in the model
- ``--path`` for ``create``/``list`` must resolve to a Classifier element
- ``--path`` + ``--name`` for ``delete``/``view``/``update`` must resolve to a
  classifier, and the operation name must exist within that classifier
- ``--guid`` must resolve to an existing element, and its ``metaClass`` must
  match ``Operation`` for ``delete``/``view``/``update``
- Invalid input raises ``CliExecutionError`` with a descriptive message
- COM errors during execution are wrapped in ``CliExecutionError``

See Also
--------

- :doc:`working_with_classes` - Class management operations
- :doc:`working_with_attributes` - Attribute management operations
- :doc:`working_with_packages` - Package management operations
