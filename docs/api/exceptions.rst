Exceptions
==========

.. automodule:: rhapsody_cli.exceptions.core
   :members:
   :undoc-members:
   :show-inheritance:

Exception Hierarchy
-------------------

.. code-block:: text

   Exception
   └── RhapsodyException
       ├── RhapsodyConnectionError
       └── RhapsodyRuntimeException

Exception Types
---------------

**RhapsodyException**
    Base class for all rhapsody-cli exceptions.

**RhapsodyConnectionError**
    Raised when connection to Rhapsody fails.
    Inherits from RhapsodyException.

    Example:

    .. code-block:: python

       try:
           app.attach()
       except RhapsodyConnectionError as e:
           print(f"Connection failed: {e}")

**RhapsodyRuntimeException**
    Raised when a COM API call fails at runtime.
    Inherits from RhapsodyException.

    Example:

    .. code-block:: python

       try:
           project = app.openProject("nonexistent.rpy")
       except RhapsodyRuntimeException as e:
           print(f"Operation failed: {e}")

Error Handling Best Practices
------------------------------

Always catch specific exceptions:

.. code-block:: python

   from rhapsody_cli.exceptions import (
       RhapsodyException,
       RhapsodyConnectionError,
       RhapsodyRuntimeException
   )

   # Specific exception handling
   try:
       app.attach()
   except RhapsodyConnectionError as e:
       # Handle connection errors
       app.launch()
   except RhapsodyRuntimeException as e:
       # Handle runtime errors
       print(f"Operation failed: {e}")
   except Exception as e:
       # Unexpected error
       print(f"Unexpected error: {e}")

Use try-finally for cleanup:

.. code-block:: python

   try:
       project = app.openProject("myproject.rpy")
       # Work with project
   except RhapsodyRuntimeException as e:
       print(f"Error: {e}")
   finally:
       # Always cleanup
       if project:
           project.close()
       app.disconnect()

See Also
--------

* :doc:`../user_guide/connecting_to_rhapsody` - Connection error handling
* :doc:`../user_guide/quickstart` - Basic error handling examples
