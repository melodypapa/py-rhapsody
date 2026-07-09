.. rhapsody-cli documentation master file

Welcome to rhapsody-cli's Documentation
========================================

rhapsody-cli is a Pythonic wrapper around the IBM Rhapsody COM API, providing a complete Python interface to the Rhapsody modeling tool. It mirrors the Rhapsody Java API, enabling developers to programmatically interact with Rhapsody models and projects.

**Current Version**: 0.1.0
**Python Requirements**: >= 3.8
**License**: MIT
**Platform**: Windows (requires IBM Rhapsody installation)

.. image:: https://badge.fury.io/py/rhapsody-cli.svg
   :target: https://badge.fury.io/py/rhapsody-cli
   :alt: PyPI version

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: https://rhapsody-cli.readthedocs.io/en/latest/
   :alt: Documentation Status

.. contents:: Table of Contents
   :depth: 2
   :local:
   :backlinks: none

Overview
--------

rhapsody-cli provides a comprehensive Python interface to the IBM Rhapsody UML/SysML modeling tool through its COM (Component Object Model) API. It enables developers to:

* Programmatically create and modify Rhapsody models
* Access model elements (classes, packages, diagrams, etc.)
* Manage projects and resources
* Automate modeling workflows
* Build custom tools and integrations

Key Features
------------

* **Complete API Wrapping**: Mirrors the Rhapsody Java API for familiar interface
* **Element Management**: Create, read, update, and delete model elements (classes, attributes, operations, etc.)
* **Project Control**: Open, close, and manage Rhapsody projects
* **Package Organization**: Work with packages and nested model structures
* **Diagram Support**: Access and manipulate diagrams
* **Connection Modes**: Support for attaching to existing Rhapsody instances or launching new ones
* **Error Handling**: Comprehensive error handling with meaningful error messages
* **Type Annotations**: Full type hints for IDE support and static analysis
* **CLI Tools**: Command-line interface for common tasks
* **Test-Driven**: Comprehensive test suite with 161+ tests

Architecture
------------

rhapsody-cli is organized in three layers:

1. **Core Model Wrapping** (``rhapsody_cli.models``)
   - Base class ``RPModelElement`` wraps all Rhapsody COM objects
   - Element subclasses mirror the Rhapsody Java API
   - Automatic wrapper registry for consistent object handling

2. **Application Entry Point** (``rhapsody_cli.application``)
   - ``RhapsodyApplication`` manages connection to Rhapsody
   - Supports three connection modes: attach, launch, and connect

3. **CLI Layer** (``rhapsody_cli.cli``)
   - argparse-based command-line interface
   - Command groups: project, element, io
   - Multiple output formats: table, JSON, CSV

Quick Start
-----------

Installation
~~~~~~~~~~~~

Install rhapsody-cli using pip:

.. code-block:: bash

   pip install rhapsody-cli

Or install with development dependencies:

.. code-block:: bash

   pip install -e ".[dev,cli]"

Basic Usage
~~~~~~~~~~~

Connect to Rhapsody and open a project:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.connect()  # Try to attach to existing instance, then launch if needed

   project = app.openProject("C:\\path\\to\\project.rpy")

Access model elements:

.. code-block:: python

   # Get all packages
   packages = project.getPackages()

   # Find a specific package
   package = project.findNestedPackageByName("MyPackage")

   # Get all classes in a package
   classes = package.getClasses()

   # Create a new class
   new_class = package.createClassElement("NewClass")

   # Add attributes and operations
   attribute = new_class.createAttribute("myAttribute")
   operation = new_class.createOperation("myOperation")

Close the project:

.. code-block:: python

   project.close()
   app.disconnect()

Command-Line Usage
~~~~~~~~~~~~~~~~~~~

View available commands:

.. code-block:: bash

   rhapsody-cli --help

Open a project:

.. code-block:: bash

   rhapsody-cli project open "C:\path\to\project.rpy"

List open projects:

.. code-block:: bash

   rhapsody-cli project list

Query model elements:

.. code-block:: bash

   rhapsody-cli element query

View element details:

.. code-block:: bash

   rhapsody-cli element view <element_id>

Documentation Structure
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   user_guide/installation
   user_guide/quickstart
   user_guide/connecting_to_rhapsody
   user_guide/working_with_projects
   user_guide/working_with_elements
   user_guide/working_with_packages
   user_guide/cli_tools

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/application
   api/models
   api/elements
   api/exceptions

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples/basic_operations
   examples/creating_models
   examples/advanced_workflows

.. toctree::
   :maxdepth: 2
   :caption: Additional Information:

   contributing
   license

Project Structure
-----------------

.. code-block:: text

   src/rhapsody_cli/
   ├── __init__.py                    # Public API exports
   ├── application.py                 # RhapsodyApplication entry point
   ├── exceptions/                    # Exception types
   │   ├── __init__.py
   │   └── core.py                   # RhapsodyConnectionError, RhapsodyRuntimeException
   ├── models/                        # Element wrappers
   │   ├── __init__.py
   │   ├── _core.py                  # RPModelElement, wrap(), call_com()
   │   └── elements/                 # Specific element types
   │       ├── __init__.py
   │       ├── class_.py             # RPClass
   │       ├── attribute.py          # RPAttribute
   │       ├── operation.py          # RPOperation
   │       ├── package.py            # RPPackage
   │       ├── project.py            # RPProject
   │       └── ...                   # Other element types
   ├── commands/                      # CLI command groups (argparse, class-based)
   │   ├── __init__.py
   │   ├── abstract_command.py       # AbstractCommand base class
   │   ├── element_command.py        # ElementCommand
   │   └── project_command.py        # ProjectCommand
   ├── actions/                       # CLI subcommand actions (argparse, class-based)
   │   ├── __init__.py
   │   ├── abstract_action.py        # AbstractAction, RhapsodyContextAction, ElementManagementAction
   │   ├── element_action.py         # ElementAddAction, ElementViewAction, ElementQueryAction, ElementDeleteAction
   │   └── project_action.py         # Project subcommand actions
   └── cli/                           # CLI entry point and support
       ├── main.py                   # Entry point (re-exports cli.main)
       ├── cli.py                    # main() dispatcher
       ├── context.py                # RhapsodyContext (state management)
       ├── formatters.py             # OutputFormatter (table/JSON/CSV)
       └── logging_config.py         # CliLoggingConfigurator

Supported Element Types
-----------------------

**Basic Elements**

* Project (RPProject)
* Package (RPPackage)
* Class (RPClass)
* Actor (RPActor)
* UseCase (RPUseCase)
* Instance (RPInstance)

**Structural Elements**

* Attribute (RPAttribute)
* Operation (RPOperation)
* Parameter (RPParameter)
* Classifier (RPClassifier)

**Behavioral Elements**

* Diagram (RPDiagram)
* Statechart (RPStatechart)
* Activity (RPActivity)
* Sequence (RPSequence)

**Type System**

* Requirement (RPRequirement)

Platform Requirements
---------------------

* **Operating System**: Windows (Rhapsody COM API is Windows-specific)
* **Python**: 3.8 or higher
* **IBM Rhapsody**: Must be installed on the system
* **COM Dependencies**: pywin32 (automatically installed)

Contributing
------------

Contributions are welcome! Please see :doc:`contributing` for guidelines on how to contribute to rhapsody-cli.

License
-------

rhapsody-cli is licensed under the MIT License. See :doc:`license` for details.

Links
-----

* `GitHub Repository <https://github.com/melodypapa/rhapsody-cli>`_
* `PyPI Package <https://pypi.org/project/rhapsody-cli/>`_
* `IBM Rhapsody Official Website <https://www.ibm.com/products/rhapsody>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
