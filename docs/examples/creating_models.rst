Creating Models
===============

This guide shows how to create complete model structures from scratch.

Create a Simple Model
---------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_simple_model():
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("new_project.rpy")

           # Create package
           pkg = project.createPackageElement("Domain")

           # Create class
           cls = pkg.createClassElement("Person")

           # Add attributes
           cls.createAttribute("name", "string")
           cls.createAttribute("age", "int")
           cls.createAttribute("email", "string")

           # Add operations
           cls.createOperation("getName", "string")
           cls.createOperation("setName", "void").createParameter("name", "string")
           cls.createOperation("getAge", "int")

           print("Simple model created successfully!")

       finally:
           project.close()
           app.disconnect()

Create an Application Architecture
-----------------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_architecture():
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("architecture_project.rpy")

           # Create main package
           app_pkg = project.createPackageElement("Application")

           # Create layers
           presentation = app_pkg.createPackageElement("Presentation")
           business = app_pkg.createPackageElement("Business")
           data = app_pkg.createPackageElement("Data")

           # Presentation layer
           controller = presentation.createClassElement("Controller")
           controller.createAttribute("model", "Model")
           controller.createOperation("handleRequest", "Response")

           # Business layer
           service = business.createClassElement("Service")
           service.createAttribute("dao", "DataAccessObject")
           service.createOperation("process", "Result")

           # Data layer
           dao = data.createClassElement("DataAccessObject")
           dao.createAttribute("connection", "DatabaseConnection")
           dao.createOperation("query", "ResultSet")

           print("Architecture created with 3 layers and 3 classes")

       finally:
           project.close()
           app.disconnect()

Create a Domain Model
---------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_domain_model():
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("domain_project.rpy")

           # Create domain package
           domain = project.createPackageElement("Domain")

           # Create Entity base class
           entity = domain.createClassElement("Entity")
           entity.createAttribute("id", "UUID")
           entity.createAttribute("createdAt", "DateTime")
           entity.createOperation("getId", "UUID")

           # Create User class
           user = domain.createClassElement("User")
           user.createAttribute("email", "string")
           user.createAttribute("password", "string")
           user.createAttribute("firstName", "string")
           user.createAttribute("lastName", "string")
           user.createAttribute("roles", "List<Role>")

           user.createOperation("authenticate", "boolean").createParameter("password", "string")
           user.createOperation("hasRole", "boolean").createParameter("role", "Role")
           user.createOperation("getFullName", "string")

           # Create Role class
           role = domain.createClassElement("Role")
           role.createAttribute("name", "string")
           role.createAttribute("permissions", "List<Permission>")
           role.createOperation("hasPermission", "boolean").createParameter("perm", "Permission")

           # Create Permission class
           perm = domain.createClassElement("Permission")
           perm.createAttribute("name", "string")
           perm.createAttribute("description", "string")

           print("Domain model created with 4 classes")
           print("  - Entity (base)")
           print("  - User")
           print("  - Role")
           print("  - Permission")

       finally:
           project.close()
           app.disconnect()

Create with Relationships
--------------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def create_model_with_relationships():
       """Create classes with associations"""
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("relationships_project.rpy")

           pkg = project.createPackageElement("Models")

           # Create Author class
           author = pkg.createClassElement("Author")
           author.createAttribute("name", "string")
           author.createAttribute("email", "string")

           # Create Book class
           book = pkg.createClassElement("Book")
           book.createAttribute("title", "string")
           book.createAttribute("isbn", "string")
           book.createAttribute("publishDate", "Date")
           book.createAttribute("authors", "List<Author>")

           # Create Library class
           library = pkg.createClassElement("Library")
           library.createAttribute("name", "string")
           library.createAttribute("location", "string")
           library.createAttribute("books", "List<Book>")

           library.createOperation("addBook", "void").createParameter("book", "Book")
           library.createOperation("findBook", "Book").createParameter("title", "string")
           library.createOperation("borrowBook", "boolean").createParameter("book", "Book")

           print("Relationship model created")

       finally:
           project.close()
           app.disconnect()

Batch Create Elements
---------------------

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   def batch_create_elements():
       """Create multiple elements efficiently"""
       app = RhapsodyApplication()
       app.connect()

       try:
           project = app.openProject("batch_project.rpy")

           pkg = project.createPackageElement("Services")

           # Define services
           services = ["UserService", "ProductService", "OrderService", "PaymentService"]

           for service_name in services:
               # Create service class
               service = pkg.createClassElement(service_name)

               # Add common attributes
               service.createAttribute("logger", "Logger")
               service.createAttribute("config", "Configuration")

               # Add common operations
               service.createOperation("initialize", "void")
               service.createOperation("shutdown", "void")
               service.createOperation("getStatus", "ServiceStatus")

               print(f"Created: {service_name}")

           print(f"\nTotal services created: {len(services)}")

       finally:
           project.close()
           app.disconnect()

See Also
--------

* :doc:`../user_guide/working_with_elements` - Element manipulation
* :doc:`../user_guide/working_with_projects` - Project management
* :doc:`basic_operations` - Basic operation examples
