#!/usr/bin/env python3
"""
Demo: Rhapsody Project Operations

This demo demonstrates common project management operations with the Rhapsody GUI visible:
- Launching Rhapsody with GUI display
- Getting active project with activeProject()
- Listing all open projects with getProjects()
- Creating new projects in system temp folder with createNewProject()
- Saving and closing projects with save() and close()
- Reopening closed projects with openProject()
- Full project lifecycle: create -> save -> close -> reopen
- Automatic cleanup: temporary project files are deleted after demo

The Rhapsody GUI window will open and remain visible during demo execution,
allowing you to observe all operations in real-time.

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import os
import sys
import tempfile
import time
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

        if project and project._com:
            print(f"[OK] Active project found: {project.getName()}")
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
            print("[-] No active project found")
            print("  Hint: Open a project in Rhapsody or create a new one")
            return None

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to get active project: {e}")
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
            print(f"[OK] Found {len(projects)} open project(s)")

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
            print("[-] No open projects found")
            print("  Hint: Open or create a project in Rhapsody")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to list projects: {e}")


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
            print(f"[-] Project file does not exist: {project_path}")
            print("  Hint: Provide a valid path to an .rpy file")
            return None

        project = app.openProject(project_path)
        print(f"[OK] Successfully opened project: {project.getName()}")

        print("\nProject Details:")
        print(f"  - Name: {project.getName()}")
        print(f"  - Filename: {project.getFilename()}")

        return project

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to open project: {e}")
        print("  Hint: Ensure the file is a valid Rhapsody project (.rpy)")
        return None


def demo_create_new_project(app: RhapsodyApplication) -> Any:
    """Demonstrate creating a new project in system temp folder.

    Handles temp folder creation, generates unique project name with timestamp,
    creates and saves the project. The project file will be cleaned up
    (deleted) after the demo completes.

    Args:
        app: Connected RhapsodyApplication instance

    Returns:
        Project filename (full path to .rpy file) if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("Operation: Create New Project")
    print("=" * 60)

    try:
        # Get system temp directory
        temp_location = tempfile.gettempdir()
        print(f"Using temp location: {temp_location}")

        # Create temp directory if it doesn't exist
        os.makedirs(temp_location, exist_ok=True)

        # Generate unique project name with timestamp (milliseconds for uniqueness)
        timestamp = str(int(time.time() * 1000))
        project_name = f"DemoProject_{timestamp}"

        print(f"Creating new project '{project_name}' at {temp_location}...")

        project = app.createNewProject(temp_location, project_name)
        print("[OK] Successfully created new project!")

        print("\nProject Details:")
        print(f"  - Name: {project.getName()}")
        print(f"  - Filename: {project.getFilename()}")

        # Save the new project
        print("\nSaving new project...")
        project.save()
        print("[OK] Project saved")

        # Capture the filename - getFilename() may return relative path or just name
        # so construct the full absolute path using temp_location
        relative_filename = project.getFilename()

        # Build the full path to the project file
        # Rhapsody creates .rpyx files, so if no extension, add it
        if not relative_filename.endswith(".rpy") and not relative_filename.endswith(".rpyx"):
            project_file_path = os.path.join(temp_location, relative_filename + ".rpyx")
        else:
            # If it already has an extension, use it as-is with temp_location
            if os.path.isabs(relative_filename):
                project_file_path = relative_filename
            else:
                project_file_path = os.path.join(temp_location, relative_filename)

        print(f"\nProject file path: {project_file_path}")
        return project_file_path

    except Exception as e:
        print(f"[-] Failed to create project: {e}")
        print("  Hint: Ensure you have write permissions to the temp location")
        sys.exit(1)


def demo_save_and_close_project(project: Any, filename: str, cleanup: bool = True) -> None:
    """Demonstrate saving, closing, and optionally cleaning up a project.

    Args:
        project: Project object to save and close
        filename: Path to the project file (for cleanup)
        cleanup: If True, delete the project file after closing (default: True)
    """
    print("\n" + "=" * 60)
    print("Operation: Save and Close Project")
    print("=" * 60)

    if not project:
        print("[-] No project to save/close")
        return

    try:
        project_name = project.getName()

        print(f"Saving project: {project_name}...")
        project.save()
        print("[OK] Project saved")

        print(f"\nClosing project: {project_name}...")
        project.close()
        print("[OK] Project closed")

        # Clean up: delete the project file (if requested)
        if cleanup and filename and os.path.exists(filename):
            print(f"\nCleaning up: deleting {filename}...")
            os.remove(filename)
            print("[OK] Project file deleted")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to save/close project: {e}")
    except OSError as e:
        print(f"[-] Failed to delete project file: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Rhapsody Project Operations")
    print("=" * 60)

    # Connect to Rhapsody
    # Use prefer_attach=False to always launch with GUI visible
    # Use prefer_attach=True to attach to existing instance if available
    print("\nConnecting to Rhapsody...")
    try:
        # Launch Rhapsody with GUI visible (prefer_attach=False ensures we launch)
        app = RhapsodyApplication.connect(prefer_attach=False)
        print("[OK] Connected successfully")

        # Rhapsody launched via COM automation starts with the UI hidden by
        # default. Explicitly disable HiddenUI to show the GUI window.
        print("\nMaking Rhapsody GUI visible...")
        app.setHiddenUI(False)
        app.bringWindowToTop()
        print("[OK] Rhapsody GUI should now be visible")
    except RhapsodyConnectionError as e:
        print(f"[-] Failed to connect: {e}")
        sys.exit(1)

    try:
        # Demo 1: Get active project
        demo_get_active_project(app)

        # Demo 2: List all projects
        demo_list_all_projects(app)

        # Demo 3: Project Lifecycle - Create -> Close -> Reopen
        print("\n" + "=" * 60)
        print("Operation: Project Lifecycle (Create -> Close -> Reopen)")
        print("=" * 60)

        # Step 1: Create project in temp (temp folder handling is internal)
        created_project_filename = demo_create_new_project(app)

        if created_project_filename:
            # Step 2: Get active project (the one we just created)
            temp_project = app.activeProject()

            if temp_project and temp_project._com:
                # Step 3: Close the created project WITHOUT cleanup (we need the file to reopen)
                demo_save_and_close_project(temp_project, created_project_filename, cleanup=False)

                # Step 4: Reopen the project
                print("\n" + "=" * 60)
                print("Operation: Reopen Closed Project")
                print("=" * 60)
                reopened_project = demo_open_existing_project(app, created_project_filename)

                if reopened_project and reopened_project._com:
                    print("\n[OK] Successfully completed create -> close -> reopen cycle!")
                    # Step 5: Close again WITH cleanup (now we can delete the file)
                    demo_save_and_close_project(reopened_project, created_project_filename, cleanup=True)
                else:
                    print("[-] Failed to reopen project")
                    # Clean up manually if reopen failed
                    if created_project_filename and os.path.exists(created_project_filename):
                        print(f"Cleaning up failed project file: {created_project_filename}")
                        try:
                            os.remove(created_project_filename)
                        except OSError as e:
                            print(f"[-] Could not delete file: {e}")
            else:
                print("[-] Could not access created project")
        else:
            print("[-] Failed to create project in temp folder")

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
