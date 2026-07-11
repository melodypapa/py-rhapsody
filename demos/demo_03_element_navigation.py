#!/usr/bin/env python3
"""
Demo: Rhapsody Element Navigation and Querying

This demo demonstrates how to navigate and query Rhapsody model elements:
- Navigating package structure with getPackages(), getClasses()
- Querying elements with getNestedElementsByMetaClass()
- Finding specific elements with findNestedElement()
- Displaying element properties (name, type, GUID)
- Collection iteration patterns

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation and an open project
"""

import os
import sys
from typing import Any

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

DEMO_PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_project", "DemoProject.rpyx")


def demo_navigate_packages(project: Any) -> None:
    """Demonstrate navigating the package structure.

    Args:
        project: Active project object
    """
    print("\n" + "=" * 60)
    print("Navigation: Package Structure")
    print("=" * 60)

    try:
        print("Getting top-level packages...")
        packages = project.getPackages()

        if packages and len(packages) > 0:
            print(f"[OK] Found {len(packages)} top-level package(s)")

            for i, pkg in enumerate(packages, 1):
                print(f"\nPackage {i}:")
                print(f"  - Name: {pkg.getName()}")
                print(f"  - Type: {pkg.getMetaClass()}")
                print(f"  - GUID: {pkg.getGUID()}")

                # Try to get classes in this package
                try:
                    classes = pkg.getClasses()
                    if classes and len(classes) > 0:
                        print(f"  - Classes: {len(classes)}")
                        for cls in classes:
                            print(f"    - {cls.getName()}")
                except Exception as e:
                    print(f"  - Classes: Unable to retrieve ({type(e).__name__})")
        else:
            print("[-] No packages found")
            print("  Hint: The project might be empty or use a different structure")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to navigate packages: {e}")


def demo_query_by_metaclass(project: Any) -> None:
    """Demonstrate querying elements by their metaclass.

    Args:
        project: Active project object
    """
    print("\n" + "=" * 60)
    print("Query: Elements by MetaClass")
    print("=" * 60)

    metaclasses = ["Class", "Actor", "UseCase", "Package", "InterfaceItem"]

    for meta_class in metaclasses:
        try:
            print(f"\nQuerying for {meta_class} elements...")
            elements = project.getNestedElementsByMetaClass(meta_class, 1)  # 1 = recursive

            if elements and len(elements) > 0:
                print(f"[OK] Found {len(elements)} {meta_class}(es)")

                # Show first few elements
                display_count = min(5, len(elements))
                for i, element in enumerate(elements[:display_count], 1):
                    guid = element.getGUID()
                    guid_short = str(guid)[:16] if guid else "<unknown>"
                    print(f"  {i}. {element.getName()} (GUID: {guid_short}...)")

                if len(elements) > display_count:
                    print(f"  ... and {len(elements) - display_count} more")
            else:
                print(f"[-] No {meta_class} elements found")

        except RhapsodyRuntimeException as e:
            print(f"[-] Failed to query {meta_class}: {e}")


def demo_find_specific_element(project: Any) -> None:
    """Demonstrate finding specific elements.

    Args:
        project: Active project object
    """
    print("\n" + "=" * 60)
    print("Query: Find Specific Elements")
    print("=" * 60)

    # Try to find some elements known to exist in demos/demo_project
    search_names = ["User", "UserService", "Customer", "ManageUsers", "Nonexistent"]

    for name in search_names:
        found = False

        # Search for different metaclasses (recursively, since these elements
        # are nested inside packages rather than at the project's top level)
        for meta_class in ["Class", "Actor", "Package", "UseCase"]:
            try:
                print(f"\nSearching for '{name}' (type: {meta_class})...")
                element = project.findNestedElementRecursive(name, meta_class)

                if element and element._com:
                    print(f"[OK] Found: {element.getMetaClass()} '{element.getName()}'")
                    print(f"  - GUID: {element.getGUID()}")
                    print(f"  - Full path name: {element.getFullPathName()}")

                    # Try to get parent
                    try:
                        parent = element.getOwner()
                        if parent and parent._com:
                            print(f"  - Parent: {parent.getMetaClass()} '{parent.getName()}'")
                    except Exception:
                        pass

                    found = True
                    break
            except RhapsodyRuntimeException:
                print(f"  Not found as {meta_class}")

        if not found:
            print(f"[-] '{name}' not found in any searched type")


def demo_display_class_details(project: Any) -> None:
    """Demonstrate displaying detailed information about classes.

    Args:
        project: Active project object
    """
    print("\n" + "=" * 60)
    print("Navigation: Class Details")
    print("=" * 60)

    try:
        # Get a few classes to examine
        classes = project.getNestedElementsByMetaClass("Class", 1)

        if not classes or len(classes) == 0:
            print("[-] No classes found to examine")
            return

        # Show details for first 3 classes
        display_count = min(3, len(classes))
        print(f"Showing details for {display_count} class(es):\n")

        for i, cls in enumerate(classes[:display_count], 1):
            print(f"Class {i}: {cls.getName()}")
            print(f"  - GUID: {cls.getGUID()}")
            print(f"  - Full path name: {cls.getFullPathName()}")

            # Get attributes
            try:
                attributes = cls.getAttributes()
                print(f"  - Attributes: {len(attributes)}")
                for attr in attributes[:3]:  # Show first 3
                    attr_type = attr.getType()
                    type_name = attr_type.getName() if attr_type and attr_type._com else "<unresolved>"
                    print(f"    - {attr.getName()}: {type_name}")
                if len(attributes) > 3:
                    print(f"    ... and {len(attributes) - 3} more")
            except Exception as e:
                print(f"  - Attributes: Unable to retrieve ({e})")

            # Get operations
            try:
                operations = cls.getOperations()
                print(f"  - Operations: {len(operations)}")
                for op in operations[:3]:  # Show first 3
                    print(f"    - {op.getName()}(): {op.getReturnTypeDeclaration()}")
                if len(operations) > 3:
                    print(f"    ... and {len(operations) - 3} more")
            except Exception as e:
                print(f"  - Operations: Unable to retrieve ({e})")

            # Get relationships
            try:
                supers = cls.getBaseClassifiers()
                if supers and len(supers) > 0:
                    print(f"  - Base classifiers: {len(supers)}")
                    for sup in supers:
                        print(f"    - {sup.getName()}")
            except Exception as e:
                print(f"  - Base classifiers: Unable to retrieve ({e})")

            print()  # Blank line between classes

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to get class details: {e}")


def demo_collection_iteration(project: Any) -> None:
    """Demonstrate Pythonic collection iteration patterns.

    Args:
        project: Active project object
    """
    print("\n" + "=" * 60)
    print("Navigation: Collection Iteration Patterns")
    print("=" * 60)

    try:
        # Get packages collection
        packages = project.getPackages()

        if not packages or len(packages) == 0:
            print("[-] No packages found for collection demonstration")
            return

        print("Demonstrating collection operations:\n")

        # Length
        print(f"1. Collection length: {len(packages)} packages")

        # Indexing (note: COM collections are 1-based, wrapped to 0-based)
        print("\n2. Indexing access:")
        try:
            first_package = packages[0]  # 0-based Python indexing
            print(f"   - First package: {first_package.getName()}")
        except Exception as e:
            print(f"   - Indexing error: {e}")

        # Iteration
        print("\n3. Iteration:")
        for i, pkg in enumerate(packages, 1):
            print(f"   {i}. {pkg.getName()}")

        # Slicing (if supported)
        print("\n4. Slicing (first 2):")
        try:
            first_two = packages[:2]
            for pkg in first_two:
                print(f"   - {pkg.getName()}")
        except Exception as e:
            print(f"   - Slicing not supported: {e}")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed collection operations: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Rhapsody Element Navigation and Querying")
    print("=" * 60)
    print("\nThis demo opens demos/demo_project and navigates its model elements.")

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

        print(f"[OK] Active project: {project.getName()}")

        # Run navigation demos
        demo_navigate_packages(project)
        demo_query_by_metaclass(project)
        demo_find_specific_element(project)
        demo_display_class_details(project)
        demo_collection_iteration(project)

    finally:
        # Clean up
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        print("Disconnecting from Rhapsody...")
        app.quit()
        print("[OK] Disconnected successfully")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
