Quick Start
===========

5-Minute Introduction
---------------------

This guide will get you started with rhapsody-cli in just a few minutes.

Step 1: Install rhapsody-cli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install rhapsody-cli

Step 2: Connect to Rhapsody
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start a Python interpreter or create a script:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   # Create an application instance
   app = RhapsodyApplication()

   # Connect to Rhapsody (attaches to existing instance or launches new)
   app.connect()

   print("Connected to Rhapsody!")

Step 3: Open a Project
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Open a project
   project = app.openProject("C:\\path\\to\\your\\project.rpy")
   print(f"Opened project: {project.getName()}")

Step 4: Access Model Elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all packages
   packages = project.getPackages()
   for package in packages:
       print(f"Package: {package.getName()}")

   # Find a specific package
   my_package = project.findNestedPackageByName("MyPackage")
   if my_package:
       # Get all classes in the package
       classes = my_package.getClasses()
       for cls in classes:
           print(f"  Class: {cls.getName()}")

Step 5: Create Model Elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a new package
   new_package = project.createPackageElement("NewPackage")

   # Create a new class in the package
   new_class = new_package.createClassElement("MyNewClass")

   # Add an attribute
   attribute = new_class.createAttribute("myAttribute", "int")

   # Add an operation
   operation = new_class.createOperation("myOperation")

   print(f"Created: {new_class.getName()}")

Step 6: Close the Project
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Close the project
   project.close()

   # Disconnect from Rhapsody
   app.disconnect()

   print("Done!")

Complete Example
----------------

Here's a complete script that ties everything together:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def main():
       # Connect to Rhapsody
       app = RhapsodyApplication()
       app.connect()

       try:
           # Open project
           project = app.openProject("C:\\path\\to\\project.rpy")

           # List all packages and classes
           packages = project.getPackages()
           for package in packages:
               print(f"Package: {package.getName()}")
               classes = package.getClasses()
               for cls in classes:
                   print(f"  Class: {cls.getName()}")

           # Create a new package and class
           new_pkg = project.createPackageElement("Demo")
           new_cls = new_pkg.createClassElement("DemoClass")
           print(f"\nCreated: {new_cls.getName()}")

       finally:
           # Always close the project
           project.close()
           app.disconnect()

   if __name__ == "__main__":
       main()

Using the Command-Line Interface
---------------------------------

rhapsody-cli also provides a CLI for common tasks:

.. code-block:: bash

   # Show help
   rhapsody-cli --help

   # Open a project
   rhapsody-cli project open "C:\path\to\project.rpy"

   # List open projects
   rhapsody-cli project list

   # Query elements (table format)
   rhapsody-cli element query

   # Query elements (JSON format)
   rhapsody-cli --output json element query

   # Close the active project
   rhapsody-cli project close

Next Steps
----------

* Read :doc:`connecting_to_rhapsody` to learn about different connection modes
* Read :doc:`working_with_projects` to understand project management
* Read :doc:`working_with_elements` for detailed element manipulation
* Read :doc:`cli_tools` for complete CLI documentation
