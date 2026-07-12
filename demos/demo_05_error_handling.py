#!/usr/bin/env python3
"""
Demo: Rhapsody Error Handling Patterns

This demo demonstrates comprehensive error handling for Rhapsody operations:
- Connection error handling with smart connect fallback
- Project operation error handling
- Element not found scenarios
- COM error translation
- Proper cleanup after errors

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


def demo_connection_error_handling() -> Any:
    """Demonstrate connection error handling with smart connect fallback.

    Returns:
        RhapsodyApplication if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Error Handling: Connection Errors")
    print("=" * 60)

    try:
        print("Using smart connect() with built-in attach -> launch fallback")
        app = RhapsodyApplication.connect()
        print("[OK] Successfully connected to Rhapsody")
        return app

    except RhapsodyConnectionError as e:
        print("\n[-] All connection methods failed")
        print(f"  Final error: {e}")
        print("\n  Troubleshooting:")
        print("  1. Ensure Rhapsody is properly installed")
        print("  2. Check for valid Rhapsody license")
        print("  3. Verify you're running on Windows")
        print("  4. Try launching Rhapsody manually first")
        raise


def demo_project_operation_errors(app: RhapsodyApplication) -> None:
    """Demonstrate project operation error handling.

    Args:
        app: Connected RhapsodyApplication instance
    """
    print("\n" + "=" * 60)
    print("Error Handling: Project Operations")
    print("=" * 60)

    # Test 1: Try to open non-existent project
    print("\nTest 1: Opening non-existent project file")
    try:
        non_existent_path = r"C:\NonExistent\Project.rpy"
        print(f"  Attempting to open: {non_existent_path}")
        project = app.open_project(non_existent_path)
        print("  [-] Unexpected success (should have failed)")
    except RhapsodyRuntimeException as e:
        print(f"  [OK] Expected error caught: {type(e).__name__}")
        print(f"    Message: {str(e)[:80]}...")

    # Test 2: Try to create project in invalid location
    print("\nTest 2: Creating project in invalid location")
    try:
        invalid_path = r"C:\Invalid\Path\That\Does\Not\Exist"
        print(f"  Attempting to create project at: {invalid_path}")
        project = app.create_new_project(invalid_path, "TestProject")
        print("  [-] Unexpected success (should have failed)")
    except RhapsodyRuntimeException as e:
        print(f"  [OK] Expected error caught: {type(e).__name__}")
        print(f"    Message: {str(e)[:80]}...")

    # Test 3: Try to get active project when none exists
    print("\nTest 3: Getting active project (may not exist)")
    try:
        print("  Attempting to get active project")
        project = app.active_project()
        if project:
            print(f"  [OK] Active project found: {project.get_name()}")
        else:
            print("  [OK] No active project (handled gracefully)")
    except RhapsodyRuntimeException as e:
        print(f"  [OK] Error caught: {type(e).__name__}")
        print(f"    Message: {str(e)[:80]}...")


def demo_element_not_found_errors(app: RhapsodyApplication) -> None:
    """Demonstrate element not found error handling.

    Args:
        app: Connected RhapsodyApplication instance
    """
    print("\n" + "=" * 60)
    print("Error Handling: Element Not Found")
    print("=" * 60)

    project = None

    try:
        # Try to get active project first
        project = app.active_project()
        if not project:
            print("  No active project available for element operations")
            print("  Skipping element not found tests")
            return

        print(f"Using project: {project.get_name()}")

        # Test 1: Try to find non-existent element
        print("\nTest 1: Finding non-existent element")
        try:
            non_existent_name = "ThisElementDoesNotExist12345"
            print(f"  Searching for: {non_existent_name}")
            element = project.find_nested_element(non_existent_name, "Class")
            if element and element._com:
                print(f"  [-] Unexpected: Found element {element.get_name()}")
            else:
                print("  [OK] Element not found (handled gracefully)")
        except RhapsodyRuntimeException as e:
            print(f"  [OK] Error caught: {type(e).__name__}")
            print(f"    Message: {str(e)[:80]}...")

        # Test 2: Try to query elements with invalid metaclass
        print("\nTest 2: Querying with invalid metaclass")
        try:
            invalid_metaclass = "InvalidMetaClass12345"
            print(f"  Querying for: {invalid_metaclass}")
            elements = project.get_nested_elements_by_meta_class(invalid_metaclass, 1)
            if elements and len(elements) > 0:
                print(f"  [-] Unexpected: Found {len(elements)} elements")
            else:
                print("  [OK] No elements found (handled gracefully)")
        except RhapsodyRuntimeException as e:
            print(f"  [OK] Error caught: {type(e).__name__}")
            print(f"    Message: {str(e)[:80]}...")

        # Test 3: Try to access nested elements on non-container
        print("\nTest 3: Accessing nested elements on non-container")
        try:
            # Get a simple element (like an attribute) that doesn't have nested elements
            classes = project.get_nested_elements_by_meta_class("Class", 1)
            if classes and len(classes) > 0:
                test_class = classes[0]
                print(f"  Using class: {test_class.get_name()}")
                # Try to get packages from a class (should fail or return empty)
                nested = test_class.get_packages()
                print(f"  [OK] Operation handled (returned {len(nested)} items)")
        except RhapsodyRuntimeException as e:
            print(f"  [OK] Error caught: {type(e).__name__}")
            print(f"    Message: {str(e)[:80]}...")

    except RhapsodyRuntimeException as e:
        print(f"[-] Unexpected error in element tests: {e}")


def demo_safe_operation_patterns(app: RhapsodyApplication) -> None:
    """Demonstrate safe operation patterns with proper error handling.

    Args:
        app: Connected RhapsodyApplication instance
    """
    print("\n" + "=" * 60)
    print("Error Handling: Safe Operation Patterns")
    print("=" * 60)

    project = None

    try:
        # Pattern 1: Safe project access
        print("\nPattern 1: Safe project access")
        try:
            project = app.active_project()
            if project:
                print(f"  [OK] Working with project: {project.get_name()}")
            else:
                print("  [OK] No active project - continuing with other tests")
        except RhapsodyRuntimeException as e:
            print(f"  [-] Failed to get project: {e}")
            project = None

        # Pattern 2: Safe element iteration
        if project:
            print("\nPattern 2: Safe element iteration")
            try:
                classes = project.get_nested_elements_by_meta_class("Class", 1)
                print(f"  Processing {len(classes)} classes safely")

                # Limit to first 5 classes
                for i in range(min(5, len(classes))):
                    try:
                        cls = classes[i]
                        name = cls.get_name()
                        guid = cls.get_guid()
                        print(f"  {i + 1}. {name} (GUID: {guid[:8]}...)")
                    except Exception as e:
                        print(f"  {i + 1}. Error processing class: {e}")

            except RhapsodyRuntimeException as e:
                print(f"  [-] Failed to get classes: {e}")

        # Pattern 3: Safe nested operations
        if project:
            print("\nPattern 3: Safe nested operations")
            try:
                packages = project.get_packages()
                success_count = 0
                error_count = 0

                # Limit to first 3 packages
                for i in range(min(3, len(packages))):
                    try:
                        pkg = packages[i]
                        pkg_name = pkg.get_name()
                        classes = pkg.get_classes()
                        success_count += 1
                        print(f"  [OK] {pkg_name}: {len(classes)} classes")
                    except Exception as e:
                        error_count += 1
                        print(f"  [-] Error processing package: {e}")

                print(f"  Summary: {success_count} successful, {error_count} errors")

            except RhapsodyRuntimeException as e:
                print(f"  [-] Failed to get packages: {e}")

    except Exception as e:
        print(f"[-] Unexpected error in safe patterns: {e}")


def demo_cleanup_after_errors(app: RhapsodyApplication) -> None:
    """Demonstrate proper cleanup after errors.

    Args:
        app: Connected RhapsodyApplication instance
    """
    print("\n" + "=" * 60)
    print("Error Handling: Cleanup After Errors")
    print("=" * 60)

    print("Demonstrating cleanup in various scenarios:\n")

    # Scenario 1: Cleanup after successful operation
    print("Scenario 1: Cleanup after successful operation")
    try:
        project = app.active_project()
        if project:
            print(f"  [OK] Successfully worked with: {project.get_name()}")
        print("  [OK] Normal cleanup completed")
    except Exception as e:
        print(f"  [-] Error occurred: {e}")
        print("  [OK] Cleanup still executed")

    # Scenario 2: Cleanup in finally block
    print("\nScenario 2: Cleanup using finally block")
    temp_project = None
    try:
        temp_project = app.active_project()
        if temp_project:
            # Simulate some work
            print(f"  [OK] Working with: {temp_project.get_name()}")
            # Intentionally cause an error for demonstration
            raise Exception("Simulated error for cleanup demo")
    except Exception as e:
        print(f"  [-] Error caught: {e}")
    finally:
        print("  [OK] Cleanup in finally block always executes")

    # Scenario 3: Context manager pattern (recommended)
    print("\nScenario 3: Context manager pattern (recommended for production)")
    print("  Note: Consider implementing context managers for Rhapsody objects")
    print("  Example: with RhapsodyProject(app, project_path) as project:")


def demo_comprehensive_error_handling() -> None:
    """Demonstrate comprehensive error handling workflow."""
    print("\n" + "=" * 60)
    print("Error Handling: Comprehensive Workflow")
    print("=" * 60)

    app = None

    try:
        print("Step 1: Connect to Rhapsody")
        app = demo_connection_error_handling()

        if app:
            # Open the demo project first for testing
            print("\nStep 1b: Open demo project")
            try:
                project = app.open_project(DEMO_PROJECT_PATH)
                print(f"[OK] Opened project: {project.get_name()}")
            except RhapsodyRuntimeException as e:
                print(f"[-] Failed to open demo project: {e}")
                return

            print("\nStep 2: Test project operation errors")
            demo_project_operation_errors(app)

            print("\nStep 3: Test element not found errors")
            demo_element_not_found_errors(app)

            print("\nStep 4: Test safe operation patterns")
            demo_safe_operation_patterns(app)

            print("\nStep 5: Test cleanup after errors")
            demo_cleanup_after_errors(app)

    except RhapsodyConnectionError as e:
        print(f"\n[-] Fatal connection error: {e}")
        print("  Cannot proceed with demos without Rhapsody connection")
        return

    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")

    finally:
        # Final cleanup
        if app:
            print("\n" + "=" * 60)
            print("Final Cleanup")
            print("=" * 60)
            try:
                print("Disconnecting from Rhapsody...")
                app.disconnect()
                time.sleep(2)  # Allow COM object lifecycle to complete
                print("[OK] Disconnected successfully")
            except Exception as e:
                print(f"[-] Error during cleanup: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Rhapsody Error Handling Patterns")
    print("=" * 60)
    print("\nThis demo demonstrates comprehensive error handling for Rhapsody.")
    print("It includes intentional errors to show proper handling patterns.")

    try:
        demo_comprehensive_error_handling()

        print("\n" + "=" * 60)
        print("Error Handling Summary")
        print("=" * 60)
        print("[OK] All error handling patterns demonstrated")
        print("\nKey takeaways:")
        print("  1. Always use try-except blocks for Rhapsody operations")
        print("  2. Use connect() with built-in attach -> launch fallback")
        print("  3. Handle 'not found' scenarios gracefully")
        print("  4. Use finally blocks for cleanup")
        print("  5. Validate results before using them")

        print("\n" + "=" * 60)
        print("Demo completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[-] Demo failed with unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
