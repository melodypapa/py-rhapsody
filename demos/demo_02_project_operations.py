#!/usr/bin/env python3
"""
Demo: Rhapsody Project Operations

This demo demonstrates common project management operations with the Rhapsody GUI visible:
- Connecting to Rhapsody with GUI display (show_gui=True)
- Opening the shipped demos/demo_project with openProject()
- Getting active project with activeProject()
- Listing all open projects with getProjects()
- Creating new projects with createNewProject() (inside demos/demo_project, cleaned up after)
- Saving and closing projects with save() and close()
- Reopening closed projects with openProject()
- Full project lifecycle: create -> save -> close -> reopen
- Automatic cleanup: the scratch project created during the demo is deleted
  afterwards; the shipped demos/demo_project is left untouched.

The Rhapsody GUI window will open and remain visible during demo execution,
allowing you to observe all operations in real-time.

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import os
import shutil
import sys
import time
from typing import Any, Optional

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

DEMO_PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_project")
DEMO_PROJECT_PATH = os.path.join(DEMO_PROJECT_DIR, "DemoProject.rpyx")


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

            active_guid = None
            try:
                active_project = app.activeProject()
                if active_project and active_project._com:
                    active_guid = active_project.getGUID()
            except RhapsodyRuntimeException:
                pass

            for i, project in enumerate(projects, 1):
                print(f"\nProject {i}:")
                print(f"  - Name: {project.getName()}")
                print(f"  - Filename: {project.getFilename()}")
                status = "Active" if active_guid and project.getGUID() == active_guid else "Inactive"
                print(f"  - Status: {status}")
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
    """Demonstrate creating a new project inside a scratch subfolder of
    demos/demo_project.

    Generates a unique project name with a timestamp, creates and saves the
    project. The scratch subfolder (and everything in it) is deleted after
    the demo completes, so the committed demos/demo_project is left
    untouched.

    Args:
        app: Connected RhapsodyApplication instance

    Returns:
        Tuple of (scratch directory, project filename), or (None, None) on failure.
    """
    print("\n" + "=" * 60)
    print("Operation: Create New Project")
    print("=" * 60)

    try:
        # Generate a unique scratch subfolder (milliseconds for uniqueness)
        # inside demos/demo_project, so the demo doesn't touch the OS temp
        # folder and stays fully self-contained within the repository.
        timestamp = str(int(time.time() * 1000))
        scratch_dir = os.path.join(DEMO_PROJECT_DIR, f"_scratch_{timestamp}")
        os.makedirs(scratch_dir, exist_ok=True)

        project_name = f"ScratchProject_{timestamp}"
        print(f"Creating new project '{project_name}' at {scratch_dir}...")

        project = app.createNewProject(scratch_dir, project_name)
        print("[OK] Successfully created new project!")

        print("\nProject Details:")
        print(f"  - Name: {project.getName()}")
        print(f"  - Filename: {project.getFilename()}")

        # Save the new project
        print("\nSaving new project...")
        project.save()
        print("[OK] Project saved")

        # Capture the filename - getFilename() may return relative path or just name
        # so construct the full absolute path using scratch_dir
        relative_filename = project.getFilename()

        # Build the full path to the project file
        # Rhapsody creates .rpyx files, so if no extension, add it
        if not relative_filename.endswith(".rpy") and not relative_filename.endswith(".rpyx"):
            project_file_path = os.path.join(scratch_dir, relative_filename + ".rpyx")
        else:
            # If it already has an extension, use it as-is with scratch_dir
            if os.path.isabs(relative_filename):
                project_file_path = relative_filename
            else:
                project_file_path = os.path.join(scratch_dir, relative_filename)

        print(f"\nProject file path: {project_file_path}")
        return scratch_dir, project_file_path

    except Exception as e:
        print(f"[-] Failed to create project: {e}")
        print("  Hint: Ensure you have write permissions to demos/demo_project")
        return None, None


def demo_save_and_close_project(project: Any, scratch_dir: Optional[str] = None) -> None:
    """Demonstrate saving and closing a project, optionally cleaning up its
    scratch directory afterwards.

    Args:
        project: Project object to save and close
        scratch_dir: If provided, the scratch directory (and everything in
            it) is deleted after closing the project.
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

        # Clean up: delete the scratch directory (if requested)
        if scratch_dir and os.path.isdir(scratch_dir):
            print(f"\nCleaning up: deleting {scratch_dir}...")
            shutil.rmtree(scratch_dir, ignore_errors=True)
            print("[OK] Scratch directory deleted")

    except RhapsodyRuntimeException as e:
        print(f"[-] Failed to save/close project: {e}")
    except OSError as e:
        print(f"[-] Failed to delete scratch directory: {e}")


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Rhapsody Project Operations")
    print("=" * 60)

    # Connect to Rhapsody with GUI visible
    print("\nConnecting to Rhapsody...")
    try:
        # show_gui=True ensures the Rhapsody window is visible
        app = RhapsodyApplication.connect(show_gui=True)
        print("[OK] Connected successfully - Rhapsody GUI should now be visible")
    except RhapsodyConnectionError as e:
        print(f"[-] Failed to connect: {e}")
        sys.exit(1)

    try:
        # Demo 0: Open the shipped demo_project (demonstrates openProject())
        demo_project = demo_open_existing_project(app, DEMO_PROJECT_PATH)
        if not demo_project or not demo_project._com:
            print("[-] Could not open demos/demo_project; aborting demo")
            sys.exit(1)

        # Demo 1: Get active project
        demo_get_active_project(app)

        # Demo 2: List all projects
        demo_list_all_projects(app)

        # Demo 3: Project Lifecycle - Create -> Close -> Reopen
        print("\n" + "=" * 60)
        print("Operation: Project Lifecycle (Create -> Close -> Reopen)")
        print("=" * 60)

        # Step 1: Create a scratch project inside demos/demo_project
        scratch_dir, created_project_filename = demo_create_new_project(app)

        if created_project_filename:
            # Step 2: Get active project (the one we just created)
            scratch_project = app.activeProject()

            if scratch_project and scratch_project._com:
                # Step 3: Close the created project WITHOUT cleanup (we need the file to reopen)
                demo_save_and_close_project(scratch_project)

                # Step 4: Reopen the project
                print("\n" + "=" * 60)
                print("Operation: Reopen Closed Project")
                print("=" * 60)
                reopened_project = demo_open_existing_project(app, created_project_filename)

                if reopened_project and reopened_project._com:
                    print("\n[OK] Successfully completed create -> close -> reopen cycle!")
                    # Step 5: Close again WITH cleanup (now we can delete the scratch directory)
                    demo_save_and_close_project(reopened_project, scratch_dir)
                else:
                    print("[-] Failed to reopen project")
                    # Clean up manually if reopen failed
                    if scratch_dir and os.path.isdir(scratch_dir):
                        print(f"Cleaning up failed scratch directory: {scratch_dir}")
                        shutil.rmtree(scratch_dir, ignore_errors=True)
            else:
                print("[-] Could not access created project")
                if scratch_dir and os.path.isdir(scratch_dir):
                    shutil.rmtree(scratch_dir, ignore_errors=True)
        else:
            print("[-] Failed to create scratch project")

        # Note: creating/opening the scratch project above replaces the
        # active workspace, so demos/demo_project (opened earlier) is
        # already closed at this point - it was never modified, so there is
        # nothing to save and nothing left to clean up for it.

    finally:
        # Clean up
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        print("Disconnecting from Rhapsody...")
        app.disconnect()
        print("[OK] Disconnected successfully")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
