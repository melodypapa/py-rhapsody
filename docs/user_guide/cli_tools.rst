CLI Tools
=========

Overview
--------

rhapsody-cli provides a command-line interface for common Rhapsody operations. The CLI is built using Python's standard-library argparse and supports multiple output formats.

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

``project new`` - Create a New Empty Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli project new <PROJECT_LOCATION> <PROJECT_NAME>

Creates a new empty Rhapsody project in ``PROJECT_LOCATION`` and names it
``PROJECT_NAME``. The new project becomes the active project.

**Example:**

.. code-block:: bash

   rhapsody-cli project new "C:\MyModels" MyNewProject

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

Multi-Level Paths
~~~~~~~~~~~~~~~~~~

The ``--path`` option (on ``add`` and ``query``) and the ``path`` argument
(on ``view`` and ``delete``) accept "/" or "\\"-separated paths to navigate
nested packages, e.g. ``parent-pkg/pkg/child-pkg``. An optional leading
``Root`` segment is accepted and ignored. When ``--path`` is omitted on
``add`` or ``query``, the project root is used.

``element add`` - Add New Element(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element add --type TYPE --name NAME [--path PATH]
   rhapsody-cli element add --type TYPE --bulk FILE [--path PATH]

Create one new element (``--name``) or many elements at once (``--bulk``)
in the active project. ``--path`` selects the destination container;
defaults to the project root.

**Examples:**

.. code-block:: bash

   # Single element at the root
   rhapsody-cli element add --type class --name MyClass

   # Single element in a nested package
   rhapsody-cli element add --type class --name MyClass --path parent-pkg/pkg

   # Bulk-create classes from a file
   rhapsody-cli element add --type class --bulk items.txt --path pkg

``items.txt`` contains one element name per line, blank lines are skipped::

   Class1
   Class2
   Class3

Output on success::

   Added 3 items:
     ✓ Class1 created at pkg/Class1
     ✓ Class2 created at pkg/Class2
     ✓ Class3 created at pkg/Class3

Output with per-item errors (creation continues past failures)::

   Added 2/3 items. Errors:
     Line 2 (Class2): duplicate name

``element view`` - View Element Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element view --path PATH

Display detailed information about a specific element addressed by a
multi-level path.

**Example:**

.. code-block:: bash

   rhapsody-cli element view --path pkg/subpkg/MyClass
   rhapsody-cli --output json element view --path pkg/subpkg/MyClass

``element query`` - Query Model Elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element query [PATTERN] [--path PATH] [--recursive]

Query and list elements directly under ``--path`` (default: project root).
Add ``--recursive`` to include elements nested at any depth; recursive
output includes each element's full path.

**Example:**

.. code-block:: bash

   # List direct children of the root
   rhapsody-cli element query

   # List direct children of a nested package
   rhapsody-cli element query --path pkg/subpkg

   # List the entire hierarchy under a package
   rhapsody-cli element query --path pkg --recursive

   # JSON output
   rhapsody-cli --output json element query --recursive

``element delete`` - Delete Element(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rhapsody-cli element delete PATH [--recursive] [--force]

Delete the element addressed by ``PATH``. Add ``--recursive`` to also
delete every element nested within it; without ``--force`` this prompts
for confirmation showing how many nested elements will be removed.

**Example:**

.. code-block:: bash

   # Delete a single element
   rhapsody-cli element delete pkg/subpkg/MyClass

   # Delete a package and everything inside it (with confirmation prompt)
   rhapsody-cli element delete pkg/subpkg --recursive

   # Same, but skip the confirmation prompt
   rhapsody-cli element delete pkg/subpkg --recursive --force

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
