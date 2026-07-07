Installation
============

Requirements
------------

* Python >= 3.8
* pip (Python package installer)
* IBM Rhapsody installed on Windows system
* pywin32 (automatically installed as a dependency)

Installing from PyPI
--------------------

The easiest way to install rhapsody-cli is using pip:

.. code-block:: bash

   pip install rhapsody-cli

This will install rhapsody-cli and all its dependencies:

* **pywin32** - Windows COM interface bindings (Windows only)

Installing with CLI Tools
--------------------------

To use the command-line interface, install with the ``cli`` extra:

.. code-block:: bash

   pip install "rhapsody-cli[cli]"

This adds:

* **click** - CLI framework
* **tabulate** - Table formatting
* **rich** - Rich terminal output

Installing from Source
----------------------

If you prefer to install from source, clone the repository and install:

.. code-block:: bash

   git clone https://github.com/melodypapa/rhapsody-cli.git
   cd rhapsody-cli
   pip install .

Development Installation
-------------------------

For development, install the package in editable mode with all dependencies:

.. code-block:: bash

   git clone https://github.com/melodypapa/rhapsody-cli.git
   cd rhapsody-cli
   pip install -e ".[dev,cli]"

This installs:

* Development tools: pytest, ruff, black, mypy
* CLI tools: click, tabulate, rich
* Core dependencies: pywin32

This allows you to modify the code without reinstalling.

Verifying Installation
----------------------

To verify that rhapsody-cli is installed correctly, run:

.. code-block:: bash

   python -c "import rhapsody_cli; print(rhapsody_cli.__version__)"

You should see the version number printed.

You can also check the installed CLI tools:

.. code-block:: bash

   rhapsody-cli --help

Troubleshooting
---------------

Import Errors on Non-Windows Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rhapsody-cli requires Windows and IBM Rhapsody to be installed. If you're on a non-Windows system, you'll see:

.. code-block:: python

   ImportError: No module named 'win32com'

This is expected. rhapsody-cli only works on Windows with Rhapsody installed.

Rhapsody COM Interface Not Available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see an error like ``CreateObject("Rhapsody.RhapsodyApp") failed``, ensure:

* IBM Rhapsody is installed on your system
* Rhapsody is properly registered with Windows COM
* You have appropriate permissions to access the COM interface

Try restarting your terminal or system if you recently installed Rhapsody.

Permission Errors
~~~~~~~~~~~~~~~~~

If you encounter permission errors during installation, try:

.. code-block:: bash

   pip install --user rhapsody-cli

Or use a virtual environment:

.. code-block:: bash

   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install rhapsody-cli

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade rhapsody-cli

Uninstalling
------------

To uninstall rhapsody-cli:

.. code-block:: bash

   pip uninstall rhapsody-cli
