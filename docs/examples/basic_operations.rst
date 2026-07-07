Basic Operations
================

This guide provides step-by-step examples of basic rhapsody-cli operations.

Example 1: Connect and List Projects
-------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   def list_open_projects():
       app = RhapsodyApplication()

       try:
           app.connect()
           print("Connected to Rhapsody")

           # Note: The connect() returns True/False indicating success
           # To list projects, you would typically open one and query it
           
       except RhapsodyConnectionError as e:
           print(f"Connection failed: {e}")
       finally:
           app.disconnect()

   if __name__ == "__main__":
       list_open_projects()

Example 2: Open Project and List Elements
------------------------------------------

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
           print(f"\nPackages: {len(packages)}")
           for pkg in packages:
               print(f"  - {pkg.getName()}")

           # List classes
           classes = project.getClasses()
           print(f"\nClasses: {len(classes)}")
           for cls in classes:
               print(f"  - {cls.getName()}")

           # List diagrams
           diagrams = project.getDiagrams()
           print(f"\nDiagrams: {len(diagrams)}")
           for diag in diagrams:
               print(f"  - {diag.getName()}")

       except RhapsodyRuntimeException as e:
           print(f"Error: {e}")
       finally:
           project.close()
           app.disconnect()

   if __name__ == "__main__":
       explore_project("C:\\path\\to\\project.rpy")

Example 3: Create Simple Model Structure
-----------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_model():
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("C:\\path\\to\\project.rpy")

           # Create package
           models_pkg = project.createPackageElement("Models")

           # Create class
           user_class = models_pkg.createClassElement("User")

           # Add attributes
           user_class.createAttribute("id", "int")
           user_class.createAttribute("name", "string")
           user_class.createAttribute("email", "string")

           # Add operation
           op = user_class.createOperation("getId", "int")

           print("Model created:")
           print(f"  Package: {models_pkg.getName()}")
           print(f"  Class: {user_class.getName()}")
           print(f"  Attributes: 3")
           print(f"  Operations: 1")

       finally:
           project.close()
           app.disconnect()

   if __name__ == "__main__":
       create_model()

Example 4: Find and Modify Elements
------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def modify_elements():
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("C:\\path\\to\\project.rpy")

           # Find package by name
           pkg = project.findNestedPackageByName("Models")
           if pkg:
               print(f"Found package: {pkg.getName()}")

               # Find class in package
               user_class = None
               for cls in pkg.getClasses():
                   if cls.getName() == "User":
                       user_class = cls
                       break

               if user_class:
                   print(f"Found class: {user_class.getName()}")

                   # List attributes
                   for attr in user_class.getAttributes():
                       print(f"  Attribute: {attr.getName()}")

                   # List operations
                   for op in user_class.getOperations():
                       print(f"  Operation: {op.getName()}")

       finally:
           project.close()
           app.disconnect()

   if __name__ == "__main__":
       modify_elements()

Example 5: Error Handling and Recovery
---------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import (
       RhapsodyConnectionError,
       RhapsodyRuntimeException
   )

   def safe_operation():
       app = RhapsodyApplication()

       # Try to attach, fall back to launching
       try:
           app.attach()
           print("Attached to running Rhapsody instance")
       except RhapsodyConnectionError:
           print("No running instance, launching new one")
           app.launch()

       project = None
       try:
           # Try to open project
           project = app.openProject("C:\\path\\to\\project.rpy")
           print(f"Successfully opened: {project.getName()}")

       except FileNotFoundError as e:
           print(f"Project file not found: {e}")

       except RhapsodyRuntimeException as e:
           print(f"Rhapsody error: {e}")

       except Exception as e:
           print(f"Unexpected error: {e}")

       finally:
           # Always cleanup
           if project:
               try:
                   project.close()
               except:
                   pass
           app.disconnect()

   if __name__ == "__main__":
       safe_operation()

See Also
--------

* :doc:`../user_guide/quickstart` - Quick start guide
* :doc:`../user_guide/working_with_elements` - Element manipulation
* :doc:`../user_guide/working_with_projects` - Project management
