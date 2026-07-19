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
* **Test-Driven**: Comprehensive test suite with 1519 tests

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

   project = app.open_project("C:\\path\\to\\project.rpy")

Access model elements:

.. code-block:: python

   # Get all packages
   packages = project.get_packages()

   # Find a specific package
   package = project.find_nested_package_by_name("MyPackage")

   # Get all classes in a package
   classes = package.get_classes()

   # Create a new class
   new_class = package.add_class("NewClass")

   # Add attributes and operations
   attribute = new_class.add_attribute("myAttribute")
   operation = new_class.add_operation("myOperation")

Close the project:

.. code-block:: python

   project.close()
   app.disconnect()

Command-Line Usage
~~~~~~~~~~~~~~~~~~~

View available commands:

.. code-block:: bash

   rhapsody-cli --help

Project management:

.. code-block:: bash

   rhapsody-cli project new "C:\Models" NewProject
   rhapsody-cli project open "C:\path\to\project.rpy"
   rhapsody-cli project list
   rhapsody-cli project close

Package management:

.. code-block:: bash

   rhapsody-cli package create --path Sensors '{"name":"Actuators"}'
   rhapsody-cli package view --path Sensors/Actuators --format json
   rhapsody-cli package list --path Sensors --format table
   rhapsody-cli package update --path Sensors/Actuators '{"description":"Updated"}'
   rhapsody-cli package delete --path Sensors/Actuators

Class management:

.. code-block:: bash

   rhapsody-cli class create --path Sensors '{"name":"TemperatureSensor"}'
   rhapsody-cli class view --path Sensors/TemperatureSensor --format json
   rhapsody-cli class list --path Sensors
   rhapsody-cli class link --path Sensors/TemperatureSensor --add BaseSensor
   rhapsody-cli class update --path Sensors/TemperatureSensor '{"isAbstract":true}'
   rhapsody-cli class delete --path Sensors/TemperatureSensor

Attribute, Operation, and Port management:

.. code-block:: bash

   rhapsody-cli attribute create --path Sensors/TemperatureSensor '{"name":"threshold","type":"int"}'
   rhapsody-cli operation create --path Sensors/TemperatureSensor '{"name":"readValue"}'
   rhapsody-cli port create --path Sensors/TemperatureSensor '{"name":"clientPort"}'

   rhapsody-cli attribute list --path Sensors/TemperatureSensor
   rhapsody-cli attribute update --path Sensors/TemperatureSensor --name threshold '{"isStatic":true}'
   rhapsody-cli attribute delete --path Sensors/TemperatureSensor --name threshold

Documentation Structure
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   user_guide/installation
   user_guide/quickstart
   user_guide/connecting_to_rhapsody
   user_guide/working_with_projects
   user_guide/working_with_packages
   user_guide/working_with_classes
   user_guide/working_with_operations
   user_guide/working_with_attributes
   user_guide/working_with_ports
   user_guide/working_with_elements
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
   CODE_GUIDELINES

.. toctree::
   :maxdepth: 1
   :caption: Requirements:

   requirements/swr_app_requirements
   requirements/swr_cli_requirements
   requirements/swr_core_requirements
   requirements/swr_exc_requirements
   requirements/swr_pkg_requirements
   requirements/swr_cls_requirements
   requirements/swr_op_requirements
   requirements/swr_attr_requirements
   requirements/swr_port_requirements
   requirements/swr_elem_requirements
   requirements/swr_xch_requirements

.. toctree::
   :maxdepth: 1
   :caption: Test Specifications:
   :glob:

   tests/unit/*
   tests/integration/*
   tests/system/*
   tests/acceptance/*

.. toctree::
   :maxdepth: 1
   :caption: Development:

   traceability_matrix

.. toctree::
   :maxdepth: 1
   :caption: Design Specs & Plans:
   :glob:

   superpowers/specs/*
   superpowers/plans/*

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
   │   ├── core.py                   # RPModelElement, RPCollection, wrap(), call_com()
   │   ├── application.py            # RhapsodyApplication COM wrapper
   │   └── elements/                 # Specific element types
   │       ├── __init__.py
   │       ├── classifiers/          # RPClass, RPActor, RPOperation, RPAttribute, etc.
   │       ├── containment/          # RPPackage, RPProject, RPComponent, etc.
   │       ├── relations/            # RPRelation, RPGeneralization, RPPort, etc.
   │       ├── diagrams/             # RPDiagram and subclasses
   │       ├── activity/             # RPFlowchart, RPFlow, RPFlowItem
   │       ├── statemachine/         # RPStatechart, RPState, RPTransition
   │       ├── interactions/         # RPCollaboration, RPMessage
   │       ├── graphics/             # RPGraphElement, RPGraphNode
   │       ├── common/               # RPType, RPConstraint, etc.
   │       ├── values/               # RPEnumerationLiteral
   │       ├── templates/            # RPTemplateParameter, RPTemplateInstantiation
   │       ├── requirements/         # RPRequirement, RPAnnotation
   │       └── variables/            # RPVariable, RPArgument
   ├── commands/                      # CLI command groups
   │   ├── __init__.py
   │   ├── abstract_command.py       # AbstractCommand base class
   │   ├── project_command.py        # ProjectCommand
   │   ├── package_command.py        # PackageCommand
   │   ├── class_command.py          # ClassCommand
   │   ├── attribute_command.py      # AttributeCommand
   │   ├── operation_command.py      # OperationCommand
   │   └── port_command.py           # PortCommand
   ├── actions/                       # CLI subcommand actions
   │   ├── __init__.py
   │   ├── abstract_action.py        # AbstractAction, RhapsodyContextAction
   │   ├── project_action.py         # Project subcommand actions
   │   ├── package_action.py         # Package subcommand actions
   │   ├── class_action.py           # Class subcommand actions
   │   ├── attribute_action.py       # Attribute subcommand actions
   │   ├── operation_action.py       # Operation subcommand actions
   │   └── port_action.py            # Port subcommand actions
   └── cli/                           # CLI entry point and support
       ├── main.py                   # Entry point (re-exports cli.main)
       ├── cli.py                    # main() dispatcher
       ├── context.py                # RhapsodyContext (state management)
       ├── formatters.py             # OutputFormatter (table/JSON/CSV)
       └── logging_config.py         # CliLoggingConfigurator

Supported Element Types
-----------------------

The package currently wraps **50+ element types** including:

**Containment Elements**: Project, Package, Profile, Module, Configuration, Node, Component, ComponentInstance, Collaboration

**Classifier Elements**: Class, Actor, UseCase, Interface, InterfaceItem, Stereotype, Statechart, Operation, AssociationClass, Signal, Exception, Enumeration

**Relation Elements**: Relation, Instance, Dependency, Generalization, Hyperlink, AssociationRole

**Activity Elements**: Flowchart, Flow, FlowItem, DecisionNode, MergeNode, ForkNode, JoinNode

**Statechart Elements**: State, Transition, Trigger

**Interaction Elements**: Message, ClassifierRole, DiagramObject

**Leaf Elements**: Attribute, Tag, Requirement, Variable, Annotation, Constraint, EnumerationLiteral, Diagram, Comment

**Support Elements**: CodeGenerator, SearchManager, Selection, ProgressBar, File, ControlledFile

Plus **hundreds of generic methods** from `RPModelElement` available on all element types.

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
