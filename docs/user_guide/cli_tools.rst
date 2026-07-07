CLI Tools
=========

Overview
--------

rhapsody-cli provides a command-line interface for common Rhapsody operations. The CLI is built using Click and supports multiple output formats.

Getting Started
---------------

View Help
~~~~~~~~~

.. code-block:: bash

   rhapsody-cli --help

View Subcommand Help
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli project --help
   rhapsody-cli element --help
   rhapsody-cli io --help

Output Formats
--------------

The ``--output`` option controls the output format:

* ``table`` (default) - Human-readable table
* ``json`` - JSON format
* ``csv`` - Comma-separated values

Examples
~~~~~~~~

.. code-block:: bash

   # Table format (default)
   rhapsody-cli project list

   # JSON format
   rhapsody-cli --output json project list

   # CSV format
   rhapsody-cli --output csv element query

Project Commands
----------------

``project open`` - Open a Rhapsody Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli project open <PROJECT_PATH>

Opens the specified Rhapsody project file (.rpy).

**Example:**

.. code-block:: bash

   rhapsody-cli project open "C:\MyModels\myproject.rpy"

``project list`` - List Open Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli project list

Lists all currently open Rhapsody projects.

**Example:**

.. code-block:: bash

   rhapsody-cli project list
   rhapsody-cli --output json project list

``project close`` - Close Active Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli project close

Closes the currently active project.

**Example:**

.. code-block:: bash

   rhapsody-cli project close

Element Commands
----------------

``element view`` - View Element Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element view <ELEMENT_ID>

Display detailed information about a specific element.

**Example:**

.. code-block:: bash

   rhapsody-cli element view MyClass
   rhapsody-cli --output json element view MyClass

``element query`` - Query Model Elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element query [FILTER]

Query and list elements from the active project.

**Example:**

.. code-block:: bash

   # List all elements
   rhapsody-cli element query

   # With filter (if supported)
   rhapsody-cli element query --type Class

   # JSON output
   rhapsody-cli --output json element query

``element add`` - Add New Element
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element add <ELEMENT_TYPE> [OPTIONS]

Create a new element in the active project.

**Example:**

.. code-block:: bash

   rhapsody-cli element add Class --name MyClass
   rhapsody-cli element add Package --name MyPackage

IO Commands
-----------

``io import`` - Import Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli io import <FILE_PATH>

Import a model from a file.

**Example:**

.. code-block:: bash

   rhapsody-cli io import model.xml

``io export`` - Export Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli io export <FILE_PATH>

Export the active model to a file.

**Example:**

.. code-block:: bash

   rhapsody-cli io export exported_model.xml

Common Use Cases
----------------

Create a New Project with Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Open project
   rhapsody-cli project open myproject.rpy

   # Add package
   rhapsody-cli element add Package --name MyPackage

   # Add class
   rhapsody-cli element add Class --name MyClass

   # View what we created
   rhapsody-cli element query

   # Close project
   rhapsody-cli project close

Query and Export
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Open project
   rhapsody-cli project open myproject.rpy

   # Query all elements (JSON format)
   rhapsody-cli --output json element query > elements.json

   # Export model
   rhapsody-cli io export model_export.xml

   # Close project
   rhapsody-cli project close

Script Integration
------------------

Using CLI in Scripts
~~~~~~~~~~~~~~~~~~~~

Example bash script (Windows):

.. code-block:: bash

   @echo off
   REM Open project
   rhapsody-cli project open "C:\MyModels\myproject.rpy"

   REM Query elements and save to file
   rhapsody-cli --output json element query > elements.json

   REM Close project
   rhapsody-cli project close

   echo Done!

Example Python integration:

.. code-block:: python

   import subprocess
   import json

   # Query elements via CLI
   result = subprocess.run(
       ["rhapsody-cli", "--output", "json", "element", "query"],
       capture_output=True,
       text=True
   )

   if result.returncode == 0:
       elements = json.loads(result.stdout)
       print(f"Found {len(elements)} elements")
   else:
       print(f"Error: {result.stderr}")

Advanced Tips
-------------

Using Redirection
~~~~~~~~~~~~~~~~~~

Save CLI output to file:

.. code-block:: bash

   rhapsody-cli project list > projects.txt
   rhapsody-cli --output json element query > elements.json

Piping Output
~~~~~~~~~~~~~

Process output with other tools:

.. code-block:: bash

   rhapsody-cli --output json element query | python -m json.tool

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set default output format:

.. code-block:: bash

   set RHAPSODY_OUTPUT=json
   rhapsody-cli element query

Troubleshooting
---------------

Command Not Found
~~~~~~~~~~~~~~~~~~

**Problem**: ``rhapsody-cli: command not found``

**Solution**: Ensure package is installed:

.. code-block:: bash

   pip install rhapsody-cli

Project Not Found
~~~~~~~~~~~~~~~~~

**Problem**: ``Error: Project file not found``

**Solution**: Use full path to project:

.. code-block:: bash

   rhapsody-cli project open "C:\full\path\to\project.rpy"

See Also
--------

* :doc:`quickstart` - Quick start guide
* :doc:`connecting_to_rhapsody` - Connection information
