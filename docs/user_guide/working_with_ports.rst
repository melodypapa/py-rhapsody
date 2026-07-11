Working with Ports
==================

The ``port`` command provides operations for managing Rhapsody port elements
via CLI. Ports are interaction points on classifiers (classes and components)
that define the interfaces through which the classifier communicates with other
elements. The command mirrors the ``class`` and ``operation`` command structure
and adds support for port-specific features like ``portContract`` resolution,
boolean flags (``isBehavioral``, ``isReversed``), and bulk creation.

Synopsis
--------

::

   rhapsody-cli port <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple ports

delete
   Delete a port

view
   View port details

list
   List ports on a classifier

update
   Modify attributes of an existing port

port create
-----------

Create one or multiple ports with validated attributes.

**Usage:**

::

   rhapsody-cli port create --path <parent-classifier-path> [options] [attributes]

**Arguments:**

- ``--path <parent-classifier-path>`` - Parent classifier path (required).
  Must resolve to a Classifier element (Class, Component, etc.).
- ``--input <json-file>`` - JSON file with port attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single port with inline JSON::

   rhapsody-cli port create --path Sensors/TemperatureSensor '{"name":"clientPort"}'

Create port with portContract::

   rhapsody-cli port create --path Sensors/TemperatureSensor '{"name":"servicePort","portContract":"ISensorInterface"}'

Create multiple ports from file::

   rhapsody-cli port create --path Sensors/TemperatureSensor --input ports.json

**JSON Format (single port):**

::

   {
     "name": "clientPort",
     "isBehavioral": true,
     "isReversed": false,
     "portContract": "ISensorInterface",
     "description": "Client communication port"
   }

**Validated Attributes:**

- ``name`` (required) - Port name, applied via ``addPort()``
- ``isBehavioral`` - Boolean, sets via ``setIsBehavioral(1/0)``
- ``isReversed`` - Boolean, sets via ``setIsReversed(1/0)``
- ``portContract`` - Interface/Class name, resolved via
  ``findNestedClassifierRecursive()`` on the parent classifier's owner package
- ``description`` - Plain text description, applied via ``setDescription()``

Unknown fields are skipped with a warning log.

port delete
-----------

Delete a port by path + name, or by GUID.

**Usage:**

::

   rhapsody-cli port delete --path <class-path> --name <port-name>
   rhapsody-cli port delete --guid <guid>

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <port-name>`` - Port name within classifier (optional)
- ``--guid <guid>`` - Port GUID to delete
  (format: 12345678-1234-1234-1234-123456789abc)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Port``; a mismatch raises ``CliExecutionError``.

**Example:**

::

   rhapsody-cli port delete --path Sensors/TemperatureSensor --name clientPort
   rhapsody-cli port delete --guid 12345678-1234-1234-1234-123456789abc

port view
---------

View port details in various formats.

**Usage:**

::

   rhapsody-cli port view --path <class-path> --name <port-name> [options]
   rhapsody-cli port view --guid <guid> [options]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <port-name>`` - Port name within classifier (optional)
- ``--guid <guid>`` - Port GUID to view (optional)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified.

**View Fields (8):**

Name, GUID, Description, IsBehavioral, IsReversed, PortContract, MetaClass, FullPath

**Output Formats:**

Table (default)::

   Property     | Value
   -------------|---------------------
   Name         | clientPort
   GUID         | 12345678-...
   IsBehavioral | 1
   IsReversed   | 0
   PortContract | ISensorInterface
   MetaClass    | Port
   FullPath     | Sensors/TemperatureSensor/clientPort

JSON::

   {
     "name": "clientPort",
     "guid": "12345678-...",
     "description": "Client communication port",
     "isBehavioral": 1,
     "isReversed": 0,
     "portContract": "ISensorInterface",
     "metaClass": "Port",
     "fullPath": "Sensors/TemperatureSensor/clientPort"
   }

CSV (horizontal)::

   Name,GUID,Description,IsBehavioral,IsReversed,PortContract,MetaClass,FullPath
   clientPort,12345678-...,Client communication port,1,0,ISensorInterface,Port,Sensors/TemperatureSensor/clientPort

port list
---------

List ports on a classifier.

**Usage:**

::

   rhapsody-cli port list --path <class-path> [options]

**Arguments:**

- ``--path <class-path>`` - Classifier path (required). Accepts a classifier
  element (Class, Component, etc.).
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Output Formats:**

Table::

   +--------------------+
   | Name               |
   +--------------------+
   | clientPort         |
   | servicePort        |
   +--------------------+

JSON::

   ["clientPort", "servicePort"]

CSV::

   Name
   clientPort
   servicePort

port update
-----------

Modify attributes of an existing port. Only specified fields are
modified (partial update).

**Usage:**

::

   rhapsody-cli port update --path <class-path> --name <port-name> [options] [attributes]
   rhapsody-cli port update --guid <guid> [options] [attributes]

**Arguments:**

- ``--path <class-path>`` - Parent classifier path (optional)
- ``--name <port-name>`` - Port name within classifier (optional)
- ``--guid <guid>`` - Port GUID to update (optional)
- ``--input <json-file>`` - JSON file with fields to update (optional)
- ``attributes`` - Inline JSON with fields to update (required if --input not
  specified)

Exactly one of ``--path`` + ``--name`` OR ``--guid`` must be specified. When
using ``--guid``, the resolved element's ``metaClass`` is validated to be
``Port``.

**Examples:**

Update description only::

   rhapsody-cli port update --path Sensors/TemperatureSensor --name clientPort '{"description":"Updated port description"}'

Update isBehavioral and portContract::

   rhapsody-cli port update --path Sensors/TemperatureSensor --name clientPort '{"isBehavioral":true,"portContract":"INewInterface"}'

Update by GUID::

   rhapsody-cli port update --guid 12345678-1234-1234-1234-123456789abc '{"isReversed":true}'

**Updatable Attributes:**

The same validated attributes as ``create``: ``name``, ``isBehavioral``,
``isReversed``, ``portContract``, ``description``. Unknown fields are skipped
with a warning.

Examples with JSON
------------------

**Create multiple ports from JSON file (ports.json):**

::

   [
     {"name": "clientPort", "portContract": "IClientInterface"},
     {"name": "servicePort", "portContract": "IServiceInterface", "isBehavioral": true}
   ]

::

   rhapsody-cli port create --path Components/SensorComponent --input ports.json

**Export and re-import workflow:**

Step 1: Export port to JSON::

   rhapsody-cli port view --path Sensors/TemperatureSensor --name clientPort --format json --output port_template.json

Step 2: Edit port_template.json (modify name, portContract, etc.)

Step 3: Create new port from template::

   rhapsody-cli port create --path Sensors/PressureSensor port_template.json

Unknown fields (``guid``, ``metaClass``, ``fullPath``) are skipped during
create with a warning. All other fields round-trip cleanly.

Error Handling
--------------

All commands validate inputs before execution:

- ``--path`` must resolve to an existing element in the model
- ``--path`` for ``create``/``list`` must resolve to a Classifier element
- ``--path`` + ``--name`` for ``delete``/``view``/``update`` must resolve to a
  classifier, and the port name must exist within that classifier
- ``--guid`` must resolve to an existing element, and its ``metaClass`` must
  match ``Port`` for ``delete``/``view``/``update``
- ``portContract`` must resolve to an existing Interface or Class in the parent's
  owner package via ``findNestedClassifierRecursive()``
- Invalid input raises ``CliExecutionError`` with a descriptive message
- COM errors during execution are wrapped in ``CliExecutionError``

See Also
--------

- :doc:`working_with_classes` - Class management operations
- :doc:`working_with_operations` - Operation management operations
- :doc:`working_with_attributes` - Attribute management operations
- :doc:`working_with_packages` - Package management operations