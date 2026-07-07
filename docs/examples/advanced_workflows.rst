Advanced Workflows
==================

This guide covers advanced workflows and patterns for rhapsody-cli.

Batch Processing
----------------

Process Multiple Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from pathlib import Path

   def process_all_projects(projects_dir):
       """Process all .rpy files in a directory"""
       app = RhapsodyApplication()
       app.connect()

       rpy_files = list(Path(projects_dir).glob("**/*.rpy"))
       print(f"Found {len(rpy_files)} projects")

       for project_file in rpy_files:
           try:
               project = app.openProject(str(project_file))

               # Count elements
               packages = project.getPackages()
               classes = project.getClasses()

               print(f"{project_file.name}: {len(packages)} packages, {len(classes)} classes")

               project.close()

           except Exception as e:
               print(f"Error processing {project_file}: {e}")

       app.disconnect()

Export Model to Dictionary
---------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def export_model_to_dict(project):
       """Convert project model to dictionary"""
       model_data = {
           "project": project.getName(),
           "packages": [],
           "classes": []
       }

       # Export packages
       for pkg in project.getPackages():
           model_data["packages"].append({
               "name": pkg.getName(),
               "nested_packages": len(pkg.getPackages()),
               "classes": len(pkg.getClasses())
           })

       # Export classes
       for cls in project.getClasses():
           cls_data = {
               "name": cls.getName(),
               "attributes": [],
               "operations": []
           }

           # Attributes
           for attr in cls.getAttributes():
               cls_data["attributes"].append(attr.getName())

           # Operations
           for op in cls.getOperations():
               params = [p.getName() for p in op.getParameters()]
               cls_data["operations"].append({
                   "name": op.getName(),
                   "parameters": params
               })

           model_data["classes"].append(cls_data)

       return model_data

   import json

   app = RhapsodyApplication()
   app.connect()

   try:
       project = app.openProject("myproject.rpy")
       model_dict = export_model_to_dict(project)
       
       # Save to JSON
       with open("model_export.json", "w") as f:
           json.dump(model_dict, f, indent=2)
       
       print("Model exported to model_export.json")

   finally:
       project.close()
       app.disconnect()

Generate Documentation from Model
---------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def generate_model_documentation(project):
       """Generate markdown documentation from model"""
       lines = [
           f"# {project.getName()} - Model Documentation",
           "",
           "## Packages"
       ]

       for pkg in project.getPackages():
           lines.append(f"\n### {pkg.getName()}")

           classes = pkg.getClasses()
           if classes:
               lines.append(f"\n**Classes:** {len(classes)}")

               for cls in classes:
                   lines.append(f"\n#### {cls.getName()}\n")

                   attrs = cls.getAttributes()
                   if attrs:
                       lines.append("**Attributes:**")
                       for attr in attrs:
                           lines.append(f"- {attr.getName()}")

                   ops = cls.getOperations()
                   if ops:
                       lines.append("\n**Operations:**")
                       for op in ops:
                           lines.append(f"- {op.getName()}()")

       return "\n".join(lines)

   app = RhapsodyApplication()
   app.connect()

   try:
       project = app.openProject("myproject.rpy")
       doc = generate_model_documentation(project)
       
       # Save documentation
       with open("MODEL_DOCUMENTATION.md", "w") as f:
           f.write(doc)
       
       print("Documentation generated: MODEL_DOCUMENTATION.md")

   finally:
       project.close()
       app.disconnect()

Model Validation
----------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def validate_model(project):
       """Validate model for common issues"""
       issues = []

       # Check for classes without attributes or operations
       for cls in project.getClasses():
           if not cls.getAttributes() and not cls.getOperations():
               issues.append(f"Empty class: {cls.getName()}")

       # Check for operations without parameters or return type
       for cls in project.getClasses():
           for op in cls.getOperations():
               params = op.getParameters()
               if not params:
                   issues.append(f"Operation without parameters: {cls.getName()}.{op.getName()}")

       # Check for duplicate class names
       class_names = [cls.getName() for cls in project.getClasses()]
       duplicates = [name for name in set(class_names) if class_names.count(name) > 1]
       if duplicates:
           for dup in duplicates:
               issues.append(f"Duplicate class name: {dup}")

       return issues

   app = RhapsodyApplication()
   app.connect()

   try:
       project = app.openProject("myproject.rpy")
       issues = validate_model(project)

       if issues:
           print("Validation issues found:")
           for issue in issues:
               print(f"  - {issue}")
       else:
           print("Model validation passed!")

   finally:
       project.close()
       app.disconnect()

Clone Model Elements
--------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def clone_class(source_class, target_package, new_name):
       """Clone a class to another package"""
       # Create new class
       new_class = target_package.createClassElement(new_name)

       # Clone attributes
       for attr in source_class.getAttributes():
           new_class.createAttribute(attr.getName())

       # Clone operations
       for op in source_class.getOperations():
           new_op = new_class.createOperation(op.getName())
           for param in op.getParameters():
               new_op.createParameter(param.getName())

       return new_class

   app = RhapsodyApplication()
   app.connect()

   try:
       project = app.openProject("myproject.rpy")

       # Find source class
       source = None
       for cls in project.getClasses():
           if cls.getName() == "User":
               source = cls
               break

       if source:
           # Find or create target package
           target = project.findNestedPackageByName("Backup")
           if not target:
               target = project.createPackageElement("Backup")

           # Clone the class
           cloned = clone_class(source, target, "UserBackup")
           print(f"Cloned class: {cloned.getName()}")

   finally:
       project.close()
       app.disconnect()

See Also
--------

* :doc:`basic_operations` - Basic operations
* :doc:`creating_models` - Model creation
* :doc:`../user_guide/working_with_elements` - Element manipulation
