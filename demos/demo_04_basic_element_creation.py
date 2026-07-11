#!/usr/bin/env python3
"""
Demo: Basic Rhapsody Element Creation

This demo demonstrates how to create basic model elements:
- Creating packages with addPackage()
- Creating classes with addClass()
- Adding attributes to classes
- Adding operations to classes
- Setting element properties (names, descriptions)
- Cleaning up created elements before saving

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import os
import sys
import time
from typing import Any

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

DEMO_PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_project", "DemoProject.rpyx")


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
        print("[OK] Package created successfully")

        print("\nPackage Details:")
        print(f"  - Name: {new_package.getName()}")
        print(f"  - Type: {new_package.getMetaClass()}")
        print(f"  - GUID: {new_package.getGUID()}")
        print(f"  - Full path name: {new_package.getFullPathName()}")

        # Set description
        description = "Package created by rhapsody-cli demo"
        new_package.setDescription(description)
        print(f"  - Description: {new_package.getDescription()}")

        return new_package

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to create package: {e}")
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
        print("[-] No package available - cannot create class")
        return None

    try:
        class_name = "DemoClass"
        print(f"Creating class: {class_name} in package: {package.getName()}...")

        # Create the class
        new_class = package.addClass(class_name)
        print("[OK] Class created successfully")

        print("\nClass Details:")
        print(f"  - Name: {new_class.getName()}")
        print(f"  - Type: {new_class.getMetaClass()}")
        print(f"  - GUID: {new_class.getGUID()}")
        print(f"  - Full path name: {new_class.getFullPathName()}")

        # Set properties
        description = "Class created by rhapsody-cli demo"
        new_class.setDescription(description)
        print(f"  - Description: {new_class.getDescription()}")

        # Set as non-abstract (default)
        new_class.setIsAbstract(0)
        print(f"  - Is Abstract: {bool(new_class.getIsAbstract())}")

        return new_class

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to create class: {e}")
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
        print("[-] No class available - cannot add attributes")
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
            attribute.setTypeDeclaration(attr_type)

            # Set default value and description
            if attr_type == "int":
                attribute.setDefaultValue("0")
            elif attr_type == "bool":
                attribute.setDefaultValue("false")

            attribute.setDescription(attr_desc)

            print(f"  [OK] Added: {attr_name} ({attr_type})")

        # Display all attributes
        print(f"\nVerifying attributes in {cls.getName()}:")
        all_attributes = cls.getAttributes()
        for i, attr in enumerate(all_attributes, 1):
            type_decl = attr.getDeclaration()
            default = attr.getDefaultValue()
            print(f"  {i}. {attr.getName()}: {type_decl} (default: {default})")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to add attributes: {e}")


def demo_add_operations(cls: Any) -> None:
    """Demonstrate adding operations to a class.

    Args:
        cls: Class object to add operations to
    """
    print("\n" + "=" * 60)
    print("Creation: Class Operations")
    print("=" * 60)

    if not cls:
        print("[-] No class available - cannot add operations")
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
            operation.setReturnTypeDeclaration(return_type)
            operation.setDescription(op_desc)

            # Add parameters
            for param_name, param_type in parameters:
                parameter = operation.addArgument(param_name)
                parameter.setTypeDeclaration(param_type)

            print(f"  [OK] Added: {op_name}({', '.join([p[0] for p in parameters])}) -> {return_type}")

        # Display all operations
        print(f"\nVerifying operations in {cls.getName()}:")
        all_operations = cls.getOperations()
        for i, op in enumerate(all_operations, 1):
            params = op.getArguments()
            param_list = ", ".join([f"{p.getName()}: {p.getDeclaration()}" for p in params])
            return_decl = op.getReturnTypeDeclaration()
            print(f"  {i}. {op.getName()}({param_list}): {return_decl}")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to add operations: {e}")


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
        print("[-] No package available - cannot create classes")
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
            print(f"  [OK] Created: {class_name}")

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
        print(f"[-] Failed to create classes: {e}")
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
        print("[OK] Project saved successfully")

        # Verify created elements still exist
        print("\nVerifying created elements...")

        # Check for our demo package
        demo_package = project.findNestedElement("DemoPackage", "Package")
        if demo_package:
            print("[OK] DemoPackage verified")
        else:
            print("[-] DemoPackage not found")

        # Check for our demo class
        demo_class = project.findNestedElement("DemoClass", "Class")
        if demo_class:
            print("[OK] DemoClass verified")
            print(f"  - Attributes: {len(demo_class.getAttributes())}")
            print(f"  - Operations: {len(demo_class.getOperations())}")
        else:
            print("[-] DemoClass not found")

        # Count total elements
        total_classes = project.getNestedElementsByMetaClass("Class", 1)
        total_packages = project.getNestedElementsByMetaClass("Package", 1)
        print("\nProject Statistics:")
        print(f"  - Total classes: {len(total_classes)}")
        print(f"  - Total packages: {len(total_packages)}")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to save/verify: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Basic Rhapsody Element Creation")
    print("=" * 60)
    print("\nThis demo creates and cleans up demo elements in demos/demo_project.")

    # Connect to Rhapsody
    print("\nConnecting to Rhapsody...")
    try:
        app = RhapsodyApplication.connect()
        print("[OK] Connected successfully")
    except RhapsodyConnectionError as e:
        print(f"[-] Failed to connect: {e}")
        sys.exit(1)

    try:
        # Open the shipped demo project
        print(f"Opening project: {DEMO_PROJECT_PATH}...")
        project = app.openProject(DEMO_PROJECT_PATH)

        if not project or not project._com:
            print("[-] Failed to open demos/demo_project")
            sys.exit(1)

        project_name = project.getName()
        print(f"[OK] Active project: {project_name}")

        # Track created elements for cleanup
        created_elements = []

        # Run creation demos
        new_package = demo_create_package(project)
        if new_package:
            created_elements.append(new_package)

            new_class = demo_create_class(new_package)
            if new_class:
                created_elements.append(new_class)
                demo_add_attributes(new_class)
                demo_add_operations(new_class)

            created_classes = demo_create_multiple_classes(new_package)
            created_elements.extend(created_classes if created_classes else [])

        # Clean up: delete all created elements before save/close
        print("\n" + "=" * 60)
        print("Cleanup: Removing Demo Elements")
        print("=" * 60)

        for element in created_elements:
            try:
                element_name = element.getName()
                print(f"Deleting {element.getMetaClass()}: {element_name}...")
                element.deleteFromProject()
                print(f"[OK] Deleted {element_name}")
            except Exception as e:
                print(f"[!] Could not delete element: {e}")

        # Save project
        try:
            print("Saving project...")
            project.save()
            print("[OK] Project saved")
        except Exception as e:
            print(f"[-] Could not save project: {e}")

    finally:
        # Clean up
        print("\n" + "=" * 60)
        print("Cleanup: Disconnecting")
        print("=" * 60)
        print("Disconnecting from Rhapsody...")
        app.disconnect()
        time.sleep(2)  # Allow COM object lifecycle to complete
        print("[OK] Disconnected successfully")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
