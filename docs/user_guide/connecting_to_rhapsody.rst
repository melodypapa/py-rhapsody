Connecting to Rhapsody
======================

Overview
--------

rhapsody-cli provides the ``RhapsodyApplication`` class to manage connections to IBM Rhapsody. It supports three connection modes:

1. **Attach** - Connect to an existing Rhapsody instance
2. **Launch** - Start a new Rhapsody instance
3. **Connect** - Try to attach first, then launch if necessary (recommended)

Connection Modes
----------------

Attach to Existing Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``attach()`` to connect to an already running Rhapsody instance:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.attach()

This method will raise ``RhapsodyConnectionError`` if Rhapsody is not running.

Launch New Instance
~~~~~~~~~~~~~~~~~~~

Use ``launch()`` to start a new Rhapsody instance:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.launch()

Connect (Recommended)
~~~~~~~~~~~~~~~~~~~~~

Use ``connect()`` to automatically try attaching first, then launch if necessary:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   app = RhapsodyApplication()
   app.connect()  # Smart connection - attach if running, launch if not

This is the recommended approach for most use cases.

Error Handling
--------------

Connection errors are raised as ``RhapsodyConnectionError``:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   app = RhapsodyApplication()

   try:
       app.attach()
   except RhapsodyConnectionError as e:
       print(f"Failed to connect: {e}")
       # Try launching instead
       app.launch()

Disconnecting
-------------

Always disconnect when done to free resources:

.. code-block:: python

   app.disconnect()

Or use a context manager pattern (if implemented):

.. code-block:: python

   with RhapsodyApplication() as app:
       app.connect()
       # Work with Rhapsody
       # Automatically disconnects when exiting the block

Connection Examples
-------------------

Complete Connection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication
   from rhapsody_cli.exceptions import RhapsodyConnectionError

   def connect_to_rhapsody():
       app = RhapsodyApplication()

       try:
           app.connect()
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

To work with multiple Rhapsody instances, create separate ``RhapsodyApplication`` objects:

.. code-block:: python

   from rhapsody_cli.application import RhapsodyApplication

   # Connect to existing instance
   app1 = RhapsodyApplication()
   app1.attach()

   # Launch new instance (in separate process)
   app2 = RhapsodyApplication()
   app2.launch()

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

2. Try attaching to an already-running instance instead of launching
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
