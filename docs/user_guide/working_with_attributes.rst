Working with Attributes
=======================

The ``attribute`` command provides operations for managing Rhapsody attribute
elements via CLI. Attributes are structural features of classifiers (classes
and interfaces) and represent the data fields/properties of the classifier.
The command mirrors the ``class`` command structure and adds support for
attribute-specific features like ``type`` resolution, ``defaultValue``,
``multiplicity``, and ``declaration``.

Synopsis
--------

::

   rhapsody-cli attribute <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple attributes

delete
   Delete an attribute

view
   View attribute details

list
   List attributes on a classifier

update
   Modify attributes of an existing attribute

attribute create
----------------

Create one or multiple attributes with validated attributes.

**Usage:**

::

   rhapsody-cli attribute create --path <parent-classifier-path> [options] [attributes]

**Arguments:**

- ``--path <parent-classifier-path>`` - Parent classifier path (required).
  Must resolve to a Classifier element (Class, Interface, etc.).
- ``--input <json-file>`` - JSON file with attribute definitions (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single attribute with inline JSON::

   rhapsody-cli attribute create --path Sensors/TemperatureSensor '{"name":"threshold","type":"double"}'

Create multiple attributes from file::

   rhapsody-cli attribute create --path Sensors/TemperatureSensor --input attributes.json

**JSON Format (single attribute):**

::

   {
     "name": "threshold",
     "type": "double",
     "defaultValue": "0.0",
     "multiplicity": "1",
     "isStatic": false,
     "visibility": "private",
     "declaration": "double threshold;",
     "description": "Sensor threshold value"
   }

**Validated Attributes:**

- ``name`` (required) - Attribute name, applied via ``addAttribute()``
- ``type`` - Type name string, resolved via
  ``findNestedClassifierRecursive()`` on the parent classifier's package and
  applied via ``setType()``
- ``defaultValue`` - Default value, applied via ``setDefaultValue()``
- ``multiplicity`` - Multiplicity string, applied via ``setMultiplicity()``
- ``isStatic`` - Boolean, sets via ``setIsStatic(1/0)``
- ``visibility`` - Visibility string (e.g. ``public``, ``private``),
  applied via ``setVisibility()``
- ``declaration`` - Declaration string, applied via ``setDeclaration()``
- ``description`` - Plain text description, applied via ``setDescription()``

Unknown fields are skipped with a warning log.

attribute delete
----------------

Delete an attribute by path + name, or by GUID.

**Usage:**

::

   rhapsody-cli attribute delete --path <class-path> --name <attribute-name>
   rhapsody-cli attribute delete --guid <guid>

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <attribute-name>`` - Attribute name within class (optional)
- ``--guid <guid>`` - Attribute GUID to delete
  (format: 12345678-1234-1234-1234-123456789abc)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Attribute``; a mismatch raises ``CliExecutionError``.

**Example:**

::

   rhapsody-cli attribute delete --path Sensors/TemperatureSensor --name threshold
   rhapsody-cli attribute delete --guid 12345678-1234-1234-1234-123456789abc

attribute view
--------------

View attribute details in various formats.

**Usage:**

::

   rhapsody-cli attribute view --path <class-path> --name <attribute-name> [options]
   rhapsody-cli attribute view --guid <guid> [options]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <attribute-name>`` - Attribute name within class (optional)
- ``--guid <guid>`` - Attribute GUID to view (optional)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified.

**View Fields (11):**

Name, GUID, Description, Type, DefaultValue, Multiplicity, IsStatic,
Visibility, Declaration, MetaClass, FullPath

**Output Formats:**

Table (default)::

   Property       | Value
   ---------------|---------------------
   Name           | threshold
   GUID           | 12345678-...
   Type           | double
   DefaultValue   | 0.0
   Multiplicity   | 1
   IsStatic       | 0
   Visibility     | private
   Declaration    | double threshold;

JSON::

   {
     "name": "threshold",
     "guid": "12345678-...",
     "type": "double",
     "defaultValue": "0.0",
     "multiplicity": "1",
     "isStatic": 0,
     "visibility": "private",
     "declaration": "double threshold;"
   }

CSV (horizontal)::

   Name,GUID,Description,Type,DefaultValue,Multiplicity,IsStatic,Visibility,Declaration,MetaClass,FullPath
   threshold,12345678-...,Sensor threshold,double,0.0,1,0,private,double threshold;,Attribute,Sensors/TemperatureSensor/threshold

attribute list
--------------

List attributes on a classifier.

**Usage:**

::

   rhapsody-cli attribute list --path <class-path> [options]

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
   | threshold          |
   | unit               |
   +--------------------+

JSON::

   ["threshold", "unit"]

CSV::

   Name
   threshold
   unit

attribute update
----------------

Modify attributes of an existing attribute. Only specified fields are
modified (partial update).

**Usage:**

::

   rhapsody-cli attribute update --path <class-path> --name <attribute-name> [options] [attributes]
   rhapsody-cli attribute update --guid <guid> [options] [attributes]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <attribute-name>`` - Attribute name within class (optional)
- ``--guid <guid>`` - Attribute GUID to update (optional)
- ``--input <json-file>`` - JSON file with fields to update (optional)
- ``attributes`` - Inline JSON with fields to update (required if --input not
  specified)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Attribute``.

**Examples:**

Update defaultValue only::

   rhapsody-cli attribute update --path Sensors/TemperatureSensor --name threshold '{"defaultValue":"25.0"}'

Update visibility and multiplicity::

   rhapsody-cli attribute update --path Sensors/TemperatureSensor --name threshold '{"visibility":"protected","multiplicity":"0..1"}'

Update by GUID::

   rhapsody-cli attribute update --guid 12345678-1234-1234-1234-123456789abc '{"defaultValue":"10.0"}'

**Updatable Attributes:**

The same validated attributes as ``create``: ``name``, ``type``,
``defaultValue``, ``multiplicity``, ``isStatic``, ``visibility``,
``declaration``, ``description``. Unknown fields are skipped with a warning.

Workflow: Attribute Cloning
---------------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export attribute to JSON::

   rhapsody-cli attribute view --path Sensors/TemperatureSensor --name threshold --format json --output template.json

**Step 2:** Edit template.json (modify name, type, etc.)

**Step 3:** Create new attribute from template::

   rhapsody-cli attribute create --path Sensors/PressureSensor template.json

Unknown fields (``guid``, ``metaClass``, ``fullPath``) are skipped during
create with a warning. All other fields round-trip cleanly.

Error Handling
--------------

All commands validate inputs before execution:

- ``--path`` must resolve to an existing element in the model
- ``--path`` for ``create``/``list`` must resolve to a Classifier element
- ``--path`` + ``--name`` for ``delete``/``view``/``update`` must resolve to a
  classifier, and the attribute name must exist within that classifier
- ``--guid`` must resolve to an existing element, and its ``metaClass`` must
  match ``Attribute`` for ``delete``/``view``/``update``
- Invalid input raises ``CliExecutionError`` with a descriptive message
- COM errors during execution are wrapped in ``CliExecutionError``

See Also
--------

- :doc:`working_with_classes` - Class management operations
- :doc:`working_with_operations` - Operation management operations
- :doc:`working_with_packages` - Package management operations
