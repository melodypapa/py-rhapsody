Connecting to Rhapsody
======================

Overview
--------

rhapsody-cli provides the ``RhapsodyApplication`` class to manage connections
to IBM Rhapsody. The primary entry point is ``RhapsodyApplication.connect()``,
which handles both attaching to a running instance and launching a new one.

Connection Modes
----------------

Smart Connect (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``connect()`` to automatically try attaching to an existing instance first,
then launch a new instance if necessary:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication.connect()  # Try attach, fall back to launch
   # ... work with Rhapsody ...
   app.disconnect()

Attach-Only Mode
~~~~~~~~~~~~~~~~

Use ``connect(attach_only=True)`` to require an already-running Rhapsody
instance:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication.connect(attach_only=True)
   # Raises RhapsodyConnectionError if Rhapsody is not running

Headless Launch
~~~~~~~~~~~~~~~

Use ``connect(show_gui=False)`` to launch a headless Rhapsody instance (no GUI):

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication.connect(show_gui=False)
   # Rhapsody runs without a visible GUI window

Error Handling
--------------

Connection errors are raised as ``RhapsodyConnectionError``:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   try:
       app = RhapsodyApplication.connect()
   except RhapsodyConnectionError as e:
       print(f"Failed to connect: {e}")

Disconnecting
-------------

Always disconnect when done to free resources:

.. code-block:: python

   app.disconnect()

The ``disconnect()`` method is the lifecycle pair of ``connect()``. Internally
it calls ``quit()`` on the COM object.

Connection Examples
-------------------

Complete Connection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   def connect_to_rhapsody():
       try:
           app = RhapsodyApplication.connect()
           print("Successfully connected to Rhapsody")
           return app
       except RhapsodyConnectionError as e:
           print(f"Failed to connect to Rhapsody: {e}")
           return None

   if __name__ == "__main__":
       app = connect_to_rhapsody()
       if app:
           try:
               # Do work here
               pass
           finally:
               app.disconnect()

Multiple Instance Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To work with multiple Rhapsody instances, create separate
``RhapsodyApplication`` objects:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   # Connect to existing instance (will fail if not running)
   app1 = RhapsodyApplication.connect(attach_only=True)

   # Launch a new instance with GUI visible
   app2 = RhapsodyApplication.connect()

   # Now you can work with both instances
   project1 = app1.openProject("project1.rpy")
   project2 = app2.openProject("project2.rpy")

   # Don't forget to clean up
   project1.close()
   project2.close()
   app1.disconnect()
   app2.disconnect()

Platform Requirements
---------------------

* **Windows**: rhapsody-cli only works on Windows (Rhapsody COM API requirement)
* **Rhapsody Installation**: IBM Rhapsody must be installed on the system
* **COM Availability**: Rhapsody must be properly registered with Windows COM
* **Permissions**: User must have appropriate permissions to launch/access Rhapsody

Troubleshooting
---------------

Connection Refused
~~~~~~~~~~~~~~~~~~

**Problem**: ``RhapsodyConnectionError: Connection to Rhapsody failed``

**Solutions**:

1. Verify IBM Rhapsody is installed:

   .. code-block:: bash

      dir "C:\Program Files*\IBM\Rhapsody"

2. Try launching Rhapsody manually first, then use ``connect(attach_only=True)``
3. Restart Rhapsody
4. Restart your terminal or IDE

COM Not Available
~~~~~~~~~~~~~~~~~

**Problem**: ``ImportError: No module named 'win32com'``

**Solution**: Install pywin32:

   .. code-block:: bash

      pip install pywin32

Non-Windows System
~~~~~~~~~~~~~~~~~~

**Problem**: Script runs on Linux/macOS

**Solution**: rhapsody-cli requires Windows. Use a Windows machine or virtual machine.
