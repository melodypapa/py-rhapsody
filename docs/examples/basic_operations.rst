Basic Operations
================

This guide provides step-by-step examples of basic rhapsody-cli operations.

Example 1: Connect and List Projects
-------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   def list_open_projects():
       try:
           # Smart connection: tries to attach, falls back to launch
           app = RhapsodyApplication.connect()
           print("Connected to Rhapsody")

           # Get all open projects
           projects = app.getProjects()
           print(f"Open projects: {len(projects)}")

           for project in projects:
               print(f"  - {project.getName()}")

           # Get active project
           active_project = app.activeProject()
           if active_project:
               print(f"Active project: {active_project.getName()}")

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
       app = RhapsodyApplication.connect()

       try:
           # Open project
           project = app.openProject(project_path)
           print(f"Opened: {project.getName()}")

           # List packages
           packages = project.getPackages()
           print(f"\nPackages: {len(packages)}")
           for pkg in packages:
               print(f"  - {pkg.getName()}")

           # List classes (recursive search)
           classes = project.getNestedElementsByMetaClass("Class", 1)
           print(f"\nClasses: {len(classes)}")
           for cls in classes:
               print(f"  - {cls.getName()}")

           # List diagrams
           diagrams = project.getNestedElementsByMetaClass("Diagram", 1)
           print(f"\nDiagrams: {len(diagrams)}")
           for diag in diagrams:
               print(f"  - {diag.getName()}")

       except RhapsodyRuntimeException as e:
           print(f"Error: {e}")
       finally:
           app.disconnect()

   if __name__ == "__main__":
       explore_project("C:\\path\\to\\project.rpy")

Example 3: Create Simple Model Structure
-----------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_model():
       app = RhapsodyApplication.connect()

       try:
           project = app.openProject("C:\\path\\to\\project.rpy")

           # Create package
           models_pkg = project.addPackage("Models")

           # Create class
           user_class = models_pkg.addClass("User")

           # Add attributes
           user_class.addAttribute("id", "int")
           user_class.addAttribute("name", "string")
           user_class.addAttribute("email", "string")

           # Add operation
           op = user_class.addOperation("getId")
           op.setReturnResult("int")

           print("Model created:")
           print(f"  Package: {models_pkg.getName()}")
           print(f"  Class: {user_class.getName()}")
           print(f"  Attributes: {len(user_class.getAttributes())}")
           print(f"  Operations: {len(user_class.getOperations())}")

           # Save changes
           project.save()

       finally:
           app.disconnect()

   if __name__ == "__main__":
       create_model()

Example 4: Find and Modify Elements
------------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def modify_elements():
       app = RhapsodyApplication.connect()

       try:
           project = app.openProject("C:\\path\\to\\project.rpy")

           # Find package by name
           pkg = project.findNestedElement("Models", "Package")
           if pkg:
               print(f"Found package: {pkg.getName()}")

               # Find class in package
               user_class = pkg.findNestedElement("User", "Class")
               if user_class:
                   print(f"Found class: {user_class.getName()}")

                   # List attributes
                   for attr in user_class.getAttributes():
                       print(f"  Attribute: {attr.getName()}")

                   # List operations
                   for op in user_class.getOperations():
                       print(f"  Operation: {op.getName()}")

       finally:
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
       # Smart connection: tries to attach, falls back to launching
       try:
           app = RhapsodyApplication.connect()
           print("Connected to Rhapsody")
       except RhapsodyConnectionError as e:
           print(f"Connection failed: {e}")
           return

       project = None
       try:
           # Try to open project
           try:
               project = app.openProject("C:\\path\\to\\project.rpy")
               print(f"Successfully opened: {project.getName()}")
           except RhapsodyRuntimeException as e:
               print(f"Project error: {e}")

       except Exception as e:
           print(f"Unexpected error: {e}")

       finally:
           # Always cleanup
           app.disconnect()

   if __name__ == "__main__":
       safe_operation()

See Also
--------

* :doc:`../user_guide/quickstart` - Quick start guide
* :doc:`../user_guide/working_with_elements` - Element manipulation
* :doc:`../user_guide/working_with_projects` - Project management
