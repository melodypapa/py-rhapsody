#!/usr/bin/env python3
"""
Demo: Rhapsody Project Operations

This demo demonstrates common project management operations:
- Opening existing projects with openProject()
- Creating new projects with createNewProject()
- Getting active project with activeProject()
- Listing all open projects with getProjects()
- Saving and closing projects
- Error handling for missing files

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import os
import sys
from typing import Any

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException


def demo_get_active_project(app: RhapsodyApplication) -> Any:
    """Demonstrate getting the active project.

    Args:
        app: Connected RhapsodyApplication instance

    Returns:
        Project object if found, None otherwise
    """
    print("\n" + "=" * 60)
    print("Operation: Get Active Project")
    print("=" * 60)

    try:
        print("Getting active project from Rhapsody...")
        project = app.activeProject()

        if project:
            print(f"✓ Active project found: {project.getName()}")
            print("\nProject Details:")
            print(f"  - Name: {project.getName()}")
            print(f"  - Filename: {project.getFilename()}")
            print(f"  - GUID: {project.getGUID()}")

            # Get some basic statistics
            try:
                packages = project.getPackages()
                classes = project.getNestedElementsByMetaClass("Class", 1)
                print(f"  - Packages: {len(packages)}")
                print(f"  - Classes (total): {len(classes)}")
            except Exception as e:
                print(f"  - Statistics unavailable: {e}")

            return project
        else:
            print("✗ No active project found")
            print("  Hint: Open a project in Rhapsody or create a new one")
            return None

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to get active project: {e}")
        return None


def demo_list_all_projects(app: RhapsodyApplication) -> None:
    """Demonstrate listing all open projects.

    Args:
        app: Connected RhapsodyApplication instance
    """
    print("\n" + "=" * 60)
    print("Operation: List All Open Projects")
    print("=" * 60)

    try:
        print("Getting all open projects...")
        projects = app.getProjects()

        if projects and len(projects) > 0:
            print(f"✓ Found {len(projects)} open project(s)")

            for i, project in enumerate(projects, 1):
                print(f"\nProject {i}:")
                print(f"  - Name: {project.getName()}")
                print(f"  - Filename: {project.getFilename()}")
                try:
                    is_active = project.getIsActive()
                    status = "Active" if is_active else "Inactive"
                    print(f"  - Status: {status}")
                except Exception:
                    print("  - Status: Unable to determine")
        else:
            print("✗ No open projects found")
            print("  Hint: Open or create a project in Rhapsody")

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to list projects: {e}")


def demo_open_existing_project(app: RhapsodyApplication, project_path: str) -> Any:
    """Demonstrate opening an existing project.

    Args:
        app: Connected RhapsodyApplication instance
        project_path: Path to the .rpy file

    Returns:
        Project object if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Operation: Open Existing Project")
    print("=" * 60)

    try:
        print(f"Attempting to open project: {project_path}")

        if not os.path.exists(project_path):
            print(f"✗ Project file does not exist: {project_path}")
            print("  Hint: Provide a valid path to an .rpy file")
            return None

        project = app.openProject(project_path)
        print(f"✓ Successfully opened project: {project.getName()}")

        print("\nProject Details:")
        print(f"  - Name: {project.getName()}")
        print(f"  - Filename: {project.getFilename()}")

        return project

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to open project: {e}")
        print("  Hint: Ensure the file is a valid Rhapsody project (.rpy)")
        return None


def demo_create_new_project(app: RhapsodyApplication, location: str, name: str) -> Any:
    """Demonstrate creating a new project.

    Args:
        app: Connected RhapsodyApplication instance
        location: Directory path for new project
        name: Name for the new project

    Returns:
        Project object if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Operation: Create New Project")
    print("=" * 60)

    try:
        print(f"Creating new project '{name}' at {location}...")

        if not os.path.exists(location):
            print(f"✗ Location does not exist: {location}")
            print("  Hint: Create the directory first or use an existing path")
            return None

        project = app.createNewProject(location, name)
        print("✓ Successfully created new project!")

        print("\nProject Details:")
        print(f"  - Name: {project.getName()}")
        print(f"  - Filename: {project.getFilename()}")

        # Save the new project
        print("\nSaving new project...")
        project.save()
        print("✓ Project saved")

        return project

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to create project: {e}")
        print("  Hint: Ensure you have write permissions to the location")
        return None


def demo_save_and_close_project(project: Any) -> None:
    """Demonstrate saving and closing a project.

    Args:
        project: Project object to save and close
    """
    print("\n" + "=" * 60)
    print("Operation: Save and Close Project")
    print("=" * 60)

    if not project:
        print("✗ No project to save/close")
        return

    try:
        project_name = project.getName()

        print(f"Saving project: {project_name}...")
        project.save()
        print("✓ Project saved")

        print(f"\nClosing project: {project_name}...")
        project.close()
        print("✓ Project closed")

    except RhapsodyRuntimeException as e:
        print(f"✗ Failed to save/close project: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Rhapsody Project Operations")
    print("=" * 60)

    # Connect to Rhapsody
    print("\nConnecting to Rhapsody...")
    try:
        app = RhapsodyApplication.connect()
        print("✓ Connected successfully")
    except RhapsodyConnectionError as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)

    try:
        # Demo 1: Get active project
        active_project = demo_get_active_project(app)

        # Demo 2: List all projects
        demo_list_all_projects(app)

        # Demo 3: Try to open an existing project (if path provided)
        # You can modify this path to test with your own project
        test_project_path = r"C:\Models\TestProject.rpy"
        if os.path.exists(test_project_path):
            demo_open_existing_project(app, test_project_path)
        else:
            print(f"\n[Skipping open existing project - file not found: {test_project_path}]")
            print("  Hint: Modify test_project_path in the script to test with your project")

        # Demo 4: Create a new project (optional - comment out if not needed)
        # You can modify these parameters to test project creation
        # demo_create_new_project(app, r"C:\Models", "DemoProject")

        # Demo 5: Save and close (if we have a project to work with)
        if active_project:
            user_input = input("\nDo you want to test save/close on the active project? (y/n): ")
            if user_input.lower() == "y":
                demo_save_and_close_project(active_project)

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
