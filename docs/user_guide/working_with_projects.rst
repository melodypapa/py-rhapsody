Working with Projects
=====================

Overview
--------

Projects are the top-level containers in Rhapsody. This guide covers how to open, manage, and work with projects using rhapsody-cli.

Opening Projects
----------------

Creating a New Empty Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using the CLI:

.. code-block:: bash

   rhapsody-cli project new C:\path\to\directory MyNewProject

Programmatically:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.connect()

   # Create a new empty project (becomes the active project)
   project = app.createNewProject("C:\\path\\to\\directory", "MyNewProject")

The ``createNewProject()`` method creates the project on disk and returns
the resulting ``RPProject`` instance (fetched via ``activeProject()``).

Opening a Project File
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.connect()

   # Open a project
   project = app.openProject("C:\\path\\to\\myproject.rpy")

The ``openProject()`` method returns an ``RPProject`` instance.

Listing Open Projects
~~~~~~~~~~~~~~~~~~~~~

Using the CLI:

.. code-block:: bash

   rhapsody-cli project list

Programmatically (if available):

.. code-block:: python

   # Get the active project
   active_project = app.getActiveProject()

Closing Projects
----------------

Always close projects to save changes and free resources:

.. code-block:: python

   project.close()

Using the CLI:

.. code-block:: bash

   rhapsody-cli project close

Project Properties
------------------

Get Project Name
~~~~~~~~~~~~~~~~

.. code-block:: python

   name = project.getName()
   print(f"Project name: {name}")

Get Project Path
~~~~~~~~~~~~~~~~

.. code-block:: python

   path = project.getPath()
   print(f"Project path: {path}")

Get Project File
~~~~~~~~~~~~~~~~

.. code-block:: python

   file = project.getFile()
   print(f"Project file: {file}")

Working with Packages
---------------------

Get All Top-Level Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   packages = project.getPackages()
   for package in packages:
       print(f"Package: {package.getName()}")

Find a Specific Package
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find by name (searches nested packages)
   package = project.findNestedPackageByName("MyPackage")

   if package:
       print(f"Found package: {package.getName()}")
   else:
       print("Package not found")

Create a New Package
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   new_package = project.createPackageElement("NewPackage")
   print(f"Created: {new_package.getName()}")

Working with Classes
---------------------

Get All Classes in Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   classes = project.getClasses()
   for cls in classes:
       print(f"Class: {cls.getName()}")

Create a New Class
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create at project level
   new_class = project.createClassElement("MyClass")

   # Or in a package
   new_class = package.createClassElement("MyClass")

Access Class Details
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   for cls in project.getClasses():
       name = cls.getName()
       attributes = cls.getAttributes()
       operations = cls.getOperations()

       print(f"Class: {name}")
       print(f"  Attributes: {len(attributes)}")
       print(f"  Operations: {len(operations)}")

Working with Diagrams
---------------------

Get All Diagrams
~~~~~~~~~~~~~~~~

.. code-block:: python

   diagrams = project.getDiagrams()
   for diagram in diagrams:
       print(f"Diagram: {diagram.getName()}")

Create a New Diagram
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   diagram = project.createDiagramElement("MyDiagram")
   print(f"Created diagram: {diagram.getName()}")

Project Management Examples
----------------------------

Complete Project Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyRuntimeException

   def explore_project(project_path):
       app = RhapsodyApplication()
       app.connect()

       try:
           # Open project
           project = app.openProject(project_path)
           print(f"Opened: {project.getName()}")

           # List packages
           packages = project.getPackages()
           print(f"\nPackages ({len(packages)}):")
           for pkg in packages:
               print(f"  - {pkg.getName()}")

           # List classes
           classes = project.getClasses()
           print(f"\nClasses ({len(classes)}):")
           for cls in classes:
               print(f"  - {cls.getName()}")

           # List diagrams
           diagrams = project.getDiagrams()
           print(f"\nDiagrams ({len(diagrams)}):")
           for diag in diagrams:
               print(f"  - {diag.getName()}")

       except RhapsodyRuntimeException as e:
           print(f"Error: {e}")

       finally:
           project.close()
           app.disconnect()

   if __name__ == "__main__":
       explore_project("C:\\path\\to\\project.rpy")

Create Project Structure
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_project_structure(project, name):
       # Create main package
       main_pkg = project.createPackageElement(name)

       # Create sub-packages
       models = main_pkg.createPackageElement("Models")
       interfaces = main_pkg.createPackageElement("Interfaces")
       behaviors = main_pkg.createPackageElement("Behaviors")

       # Create classes in Models package
       entity = models.createClassElement("Entity")
       service = models.createClassElement("Service")

       print(f"Created project structure: {name}")
       print(f"  Main Package: {main_pkg.getName()}")
       print(f"  Sub-packages: 3")
       print(f"  Classes: 2")

       return main_pkg

   app = RhapsodyApplication()
   app.connect()

   try:
       project = app.openProject("C:\\path\\to\\project.rpy")
       main = create_project_structure(project, "MyProject")
   finally:
       project.close()
       app.disconnect()

Error Handling
--------------

Handle Project Errors
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.exceptions import RhapsodyRuntimeException, RhapsodyConnectionError

   try:
       project = app.openProject(project_path)
       # Work with project
   except FileNotFoundError:
       print(f"Project file not found: {project_path}")
   except RhapsodyRuntimeException as e:
       print(f"Rhapsody error: {e}")
   except RhapsodyConnectionError as e:
       print(f"Connection error: {e}")
   finally:
       if project:
           project.close()

See Also
--------

* :doc:`working_with_elements` - Detailed guide on working with model elements
* :doc:`connecting_to_rhapsody` - Connection management
