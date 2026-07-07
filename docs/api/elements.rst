Elements
========

.. automodule:: rhapsody_cli.models.elements
   :members:
   :undoc-members:
   :show-inheritance:

Supported Element Types
-----------------------

rhapsody-cli provides wrapper classes for all major Rhapsody element types:

**Structural Elements**

* RPProject - Project container
* RPPackage - Package container
* RPClass - UML class
* RPActor - System actor
* RPUseCase - Use case
* RPInstance - Object instance
* RPDiagram - Diagram
* RPStatechart - State machine

**Behavioral Elements**

* RPAttribute - Class attribute
* RPOperation - Class operation
* RPParameter - Operation parameter
* RPClassifier - Base classifier

**Other Elements**

* RPRequirement - Requirement element
* RPConnector - Connection between elements

All element types inherit from ``RPModelElement`` and follow the same interface patterns.

See :doc:`../user_guide/working_with_elements` for usage examples.
