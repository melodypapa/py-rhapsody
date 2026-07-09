Working with Elements
=====================

Overview
--------

Model elements (classes, attributes, operations, packages, etc.) are the building blocks of Rhapsody models. This guide covers how to create, read, update, and delete elements.

Element Types
-------------

rhapsody-cli supports all major Rhapsody element types:

* **Project** - Top-level container
* **Package** - Organizational container
* **Class** - UML class
* **Attribute** - Class attribute/property
* **Operation** - Class method/operation
* **Parameter** - Operation parameter
* **Actor** - System actor
* **UseCase** - Use case
* **Instance** - Object instance
* **Diagram** - Graphical representation
* **Requirement** - Requirement element

Creating Elements
-----------------

Create a Package
~~~~~~~~~~~~~~~~

.. code-block:: python

   package = project.createPackageElement("MyPackage")

Create a Class
~~~~~~~~~~~~~~

.. code-block:: python

   # At project level
   cls = project.createClassElement("MyClass")

   # In a package
   cls = package.createClassElement("MyClass")

Create Attributes
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Basic attribute
   attr = cls.createAttribute("myAttribute")

   # With type
   attr = cls.createAttribute("myAttribute", "int")

   # With full details
   attr = cls.createAttribute("myAttribute", "int", "default_value")

Create Operations
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Basic operation
   op = cls.createOperation("myOperation")

   # With return type
   op = cls.createOperation("myOperation", "void")

Add Parameters
~~~~~~~~~~~~~~

.. code-block:: python

   # Get operation
   op = cls.getOperation("myOperation")

   # Add parameter
   param = op.createParameter("paramName", "int")

Reading Elements
----------------

Get Element Name
~~~~~~~~~~~~~~~~

.. code-block:: python

   name = element.getName()
   print(f"Element: {name}")

Get Element Properties
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   for cls in project.getClasses():
       name = cls.getName()
       attributes = cls.getAttributes()
       operations = cls.getOperations()
       print(f"{name}: {len(attributes)} attrs, {len(operations)} ops")

Find Elements by Name
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find nested package
   package = project.findNestedPackageByName("MyPackage")

   # Find class in package
   cls = package.findClassByName("MyClass")

Find Elements by CLI Path
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``rhapsody-cli element`` commands accept "/" or "\\"-separated paths
to address elements nested arbitrarily deep, instead of requiring
Python calls like ``findNestedPackageByName``:

.. code-block:: bash

   # Equivalent to: project.findNestedPackageByName("pkg").findClassByName("MyClass")
   rhapsody-cli element view --path pkg/MyClass

   # Nested two levels deep
   rhapsody-cli element view --path parent-pkg/pkg/MyClass

A path segment is matched by ``getName()`` against each level's
``getNestedElements()``. An optional leading ``Root`` segment is
accepted and ignored.

Get All Elements of Type
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all packages
   packages = project.getPackages()

   # Get all classes
   classes = project.getClasses()

   # Get all diagrams
   diagrams = project.getDiagrams()

   # Get attributes in class
   attributes = cls.getAttributes()

   # Get operations in class
   operations = cls.getOperations()

Updating Elements
-----------------

Rename an Element
~~~~~~~~~~~~~~~~~

.. code-block:: python

   cls.setName("NewClassName")

Modify Properties
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Set attribute type
   attr.setType("string")

   # Set operation return type
   op.setReturnType("boolean")

Deleting Elements
-----------------

Delete an Element
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Delete a class
   cls.delete()

   # Delete an attribute
   attr.delete()

   # Delete an operation
   op.delete()

Traversing the Model
--------------------

Get Nested Packages
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def list_all_packages(container, indent=0):
       prefix = "  " * indent
       for package in container.getPackages():
           print(f"{prefix}Package: {package.getName()}")
           list_all_packages(package, indent + 1)

   list_all_packages(project)

Get All Classes Recursively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_all_classes(container, result=None):
       if result is None:
           result = []

       # Add direct classes
       for cls in container.getClasses():
           result.append(cls)

       # Add classes in nested packages
       for package in container.getPackages():
           get_all_classes(package, result)

       return result

   all_classes = get_all_classes(project)
   print(f"Total classes: {len(all_classes)}")

List Full Class Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def print_class_details(cls, indent=0):
       prefix = "  " * indent
       print(f"{prefix}Class: {cls.getName()}")

       # Print attributes
       for attr in cls.getAttributes():
           print(f"{prefix}  Attribute: {attr.getName()}")

       # Print operations
       for op in cls.getOperations():
           print(f"{prefix}  Operation: {op.getName()}")
           for param in op.getParameters():
               print(f"{prefix}    Parameter: {param.getName()}")

   for cls in project.getClasses():
       print_class_details(cls)

Working with Element Collections
---------------------------------

.. code-block:: python

   # Get collection
   classes = project.getClasses()

   # Check if empty
   if not classes:
       print("No classes found")

   # Iterate
   for cls in classes:
       print(cls.getName())

   # Count
   count = len(classes)
   print(f"Total: {count}")

Complete Examples
-----------------

Create a Complete Model
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_model(project):
       # Create main package
       main = project.createPackageElement("Application")

       # Create domain package
       domain = main.createPackageElement("Domain")

       # Create User class
       user = domain.createClassElement("User")
       user.createAttribute("id", "int")
       user.createAttribute("name", "string")
       user.createAttribute("email", "string")

       # Create getId operation
       op = user.createOperation("getId", "int")

       # Create setName operation
       op = user.createOperation("setName", "void")
       op.createParameter("name", "string")

       # Create Service package
       services = main.createPackageElement("Services")

       # Create UserService class
       service = services.createClassElement("UserService")
       service.createAttribute("users", "List<User>")

       # Create getUser operation
       op = service.createOperation("getUser", "User")
       op.createParameter("id", "int")

       return main

   if __name__ == "__main__":
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("C:\\path\\to\\project.rpy")
           main = create_model(project)
           print("Model created successfully!")
       finally:
           project.close()
           app.disconnect()

Query and Display Model
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def display_model(project):
       print(f"Project: {project.getName()}")
       print()

       for package in project.getPackages():
           print(f"Package: {package.getName()}")

           for cls in package.getClasses():
               print(f"  Class: {cls.getName()}")

               attrs = cls.getAttributes()
               if attrs:
                   print(f"    Attributes:")
                   for attr in attrs:
                       print(f"      - {attr.getName()}")

               ops = cls.getOperations()
               if ops:
                   print(f"    Operations:")
                   for op in ops:
                       params = op.getParameters()
                       param_str = ", ".join(p.getName() for p in params)
                       print(f"      - {op.getName()}({param_str})")

Error Handling
--------------

.. code-block:: python

   from rhapsody_cli.exceptions import RhapsodyRuntimeException

   try:
       element = parent.createClassElement("MyClass")
       attr = element.createAttribute("myAttr", "int")
   except RhapsodyRuntimeException as e:
       print(f"Failed to create element: {e}")

See Also
--------

* :doc:`working_with_projects` - Project management guide
* :doc:`connecting_to_rhapsody` - Connection setup
