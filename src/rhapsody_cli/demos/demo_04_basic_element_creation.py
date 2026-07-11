#!/usr/bin/env python3
"""
Demo: Basic Rhapsody Element Creation

This demo demonstrates how to create basic model elements:
- Creating packages with addPackage()
- Creating classes with addClass()
- Adding attributes to classes
- Adding operations to classes
- Setting element properties (names, descriptions)
- Saving and verifying creation

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation and an open project
"""

import sys
from typing import Any

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException


def demo_create_package(project: Any) -> Any:
    """Demonstrate creating a new package.

    Args:
        project: Active project object

    Returns:
        New package object if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Creation: New Package")
    print("=" * 60)

    try:
        package_name = "DemoPackage"
        print(f"Creating package: {package_name}...")

        # Create the package
        new_package = project.addPackage(package_name)
        print("✓ Package created successfully")

        print("\nPackage Details:")
        print(f"  - Name: {new_package.getName()}")
        print(f"  - Type: {new_package.getMetaClass()}")
        print(f"  - GUID: {new_package.getGUID()}")
        print(f"  - Full name: {new_package.getFullName()}")

        # Set description
        description = "Package created by rhapsody-cli demo"
        new_package.setDescription(description)
        print(f"  - Description: {new_package.getDescription()}")

        return new_package

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to create package: {e}")
        print("  Hint: Ensure you have write permissions to the project")
        return None


def demo_create_class(package: Any) -> Any:
    """Demonstrate creating a new class.

    Args:
        package: Package object to create class in

    Returns:
        New class object if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Creation: New Class")
    print("=" * 60)

    if not package:
        print("✗ No package available - cannot create class")
        return None

    try:
        class_name = "DemoClass"
        print(f"Creating class: {class_name} in package: {package.getName()}...")

        # Create the class
        new_class = package.addClass(class_name)
        print("✓ Class created successfully")

        print("\nClass Details:")
        print(f"  - Name: {new_class.getName()}")
        print(f"  - Type: {new_class.getMetaClass()}")
        print(f"  - GUID: {new_class.getGUID()}")
        print(f"  - Full name: {new_class.getFullName()}")

        # Set properties
        description = "Class created by rhapsody-cli demo"
        new_class.setDescription(description)
        print(f"  - Description: {new_class.getDescription()}")

        # Set as non-abstract (default)
        new_class.setIsAbstract(0)
        print(f"  - Is Abstract: {bool(new_class.getIsAbstract())}")

        return new_class

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to create class: {e}")
        return None


def demo_add_attributes(cls: Any) -> None:
    """Demonstrate adding attributes to a class.

    Args:
        cls: Class object to add attributes to
    """
    print("\n" + "=" * 60)
    print("Creation: Class Attributes")
    print("=" * 60)

    if not cls:
        print("✗ No class available - cannot add attributes")
        return

    try:
        # Define attributes to create
        attributes = [
            ("id", "int", "Unique identifier"),
            ("name", "String", "Name of the entity"),
            ("active", "bool", "Active status flag"),
            ("count", "int", "Item counter"),
        ]

        print(f"Adding {len(attributes)} attributes to class: {cls.getName()}...")

        for attr_name, attr_type, attr_desc in attributes:
            # Create attribute
            attribute = cls.addAttribute(attr_name)
            attribute.setType(attr_type)

            # Set default value and description
            if attr_type == "int":
                attribute.setDefault("0")
            elif attr_type == "bool":
                attribute.setDefault("false")

            attribute.setDescription(attr_desc)

            print(f"  ✓ Added: {attr_name} ({attr_type})")

        # Display all attributes
        print(f"\nVerifying attributes in {cls.getName()}:")
        all_attributes = cls.getAttributes()
        for i, attr in enumerate(all_attributes, 1):
            print(f"  {i}. {attr.getName()}: {attr.getType()}")
            print(f"     Default: {attr.getDefault()}")
            print(f"     Description: {attr.getDescription()}")

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to add attributes: {e}")


def demo_add_operations(cls: Any) -> None:
    """Demonstrate adding operations to a class.

    Args:
        cls: Class object to add operations to
    """
    print("\n" + "=" * 60)
    print("Creation: Class Operations")
    print("=" * 60)

    if not cls:
        print("✗ No class available - cannot add operations")
        return

    try:
        # Define operations to create
        operations = [
            ("getId", "int", "Get the unique identifier", []),
            ("setName", "void", "Set the name of the entity", [("name", "String")]),
            ("getName", "String", "Get the name of the entity", []),
            ("isActive", "bool", "Check if entity is active", []),
            ("increment", "void", "Increment the counter", []),
        ]

        print(f"Adding {len(operations)} operations to class: {cls.getName()}...")

        for op_name, return_type, op_desc, parameters in operations:
            # Create operation
            operation = cls.addOperation(op_name)
            operation.setReturnResult(return_type)
            operation.setDescription(op_desc)

            # Add parameters
            for param_name, param_type in parameters:
                parameter = operation.addParameter(param_name)
                parameter.setType(param_type)

            print(f"  ✓ Added: {op_name}({', '.join([p[0] for p in parameters])}) -> {return_type}")

        # Display all operations
        print(f"\nVerifying operations in {cls.getName()}:")
        all_operations = cls.getOperations()
        for i, op in enumerate(all_operations, 1):
            params = op.getParameters()
            param_list = ", ".join([f"{p.getName()}: {p.getType()}" for p in params])
            print(f"  {i}. {op.getName()}({param_list}): {op.getReturnResult()}")

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to add operations: {e}")


def demo_create_multiple_classes(package: Any) -> list[Any]:
    """Demonstrate creating multiple related classes.

    Args:
        package: Package object to create classes in

    Returns:
        List of created class objects
    """
    print("\n" + "=" * 60)
    print("Creation: Multiple Related Classes")
    print("=" * 60)

    if not package:
        print("✗ No package available - cannot create classes")
        return []

    try:
        # Define classes to create
        classes_config = [
            ("User", "Represents a user in the system"),
            ("UserService", "Service for managing users"),
            ("UserRepository", "Repository for user data access"),
        ]

        created_classes = []

        print(f"Creating {len(classes_config)} classes in package: {package.getName()}...")

        for class_name, description in classes_config:
            # Create class
            new_class = package.addClass(class_name)
            new_class.setDescription(description)

            created_classes.append(new_class)
            print(f"  ✓ Created: {class_name}")

        # Create a simple inheritance relationship
        if len(created_classes) >= 2:
            print("\nCreating inheritance relationship...")
            try:
                # Make UserService inherit from a base (if we had one)
                # For now, just show that we can access the created classes
                for cls in created_classes:
                    print(f"  - {cls.getName()}: {cls.getDescription()}")
            except Exception as e:
                print(f"  Note: Relationship creation: {e}")

        return created_classes

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to create classes: {e}")
        return []


def demo_save_and_verify(project: Any) -> None:
    """Demonstrate saving and verifying created elements.

    Args:
        project: Project object to save and verify
    """
    print("\n" + "=" * 60)
    print("Verification: Save and Verify Created Elements")
    print("=" * 60)

    try:
        print("Saving project...")
        project.save()
        print("✓ Project saved successfully")

        # Verify created elements still exist
        print("\nVerifying created elements...")

        # Check for our demo package
        demo_package = project.findNestedElement("DemoPackage", "Package")
        if demo_package:
            print("✓ DemoPackage verified")
        else:
            print("✗ DemoPackage not found")

        # Check for our demo class
        demo_class = project.findNestedElement("DemoClass", "Class")
        if demo_class:
            print("✓ DemoClass verified")
            print(f"  - Attributes: {len(demo_class.getAttributes())}")
            print(f"  - Operations: {len(demo_class.getOperations())}")
        else:
            print("✗ DemoClass not found")

        # Count total elements
        total_classes = project.getNestedElementsByMetaClass("Class", 1)
        total_packages = project.getNestedElementsByMetaClass("Package", 1)
        print("\nProject Statistics:")
        print(f"  - Total classes: {len(total_classes)}")
        print(f"  - Total packages: {len(total_packages)}")

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to save/verify: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Basic Rhapsody Element Creation")
    print("=" * 60)
    print("\nThis demo creates new elements in your Rhapsody project.")
    print("⚠ Note: This will modify your active project!")

    # Connect to Rhapsody
    print("\nConnecting to Rhapsody...")
    try:
        app = RhapsodyApplication.connect()
        print("✓ Connected successfully")
    except RhapsodyConnectionError as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)

    try:
        # Get active project
        print("Getting active project...")
        project = app.activeProject()

        if not project:
            print("✗ No active project found")
            print("  Hint: Open a project in Rhapsody before running this demo")
            sys.exit(1)

        project_name = project.getName()
        print(f"✓ Active project: {project_name}")

        # Ask for user confirmation
        user_input = input(f"\nDo you want to create demo elements in '{project_name}'? (y/n): ")
        if user_input.lower() != "y":
            print("Demo cancelled by user")
            sys.exit(0)

        # Run creation demos
        new_package = demo_create_package(project)

        if new_package:
            new_class = demo_create_class(new_package)

            if new_class:
                demo_add_attributes(new_class)
                demo_add_operations(new_class)

            demo_create_multiple_classes(new_package)

            demo_save_and_verify(project)

        print("\n" + "=" * 60)
        print("Element Creation Summary")
        print("=" * 60)
        print("✓ Demo elements created successfully")
        print("  Check your Rhapsody project to see the new elements:")
        print("  - DemoPackage")
        print("    - DemoClass (with attributes and operations)")
        print("    - User, UserService, UserRepository")

    finally:
        # Clean up
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        print("Disconnecting from Rhapsody...")
        app.disconnect()  # type: ignore[attr-defined]
        print("✓ Disconnected successfully")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
