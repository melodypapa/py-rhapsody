#!/usr/bin/env python3
"""
Demo: Basic Rhapsody Connection Methods

This demo demonstrates three ways to connect to Rhapsody using the
simplified connect() API:

1. connect() - Smart connection (tries attach first, falls back to launch)
2. connect(attach_only=True) - Attach to running instance only
3. connect(show_gui=True) - Launch with GUI visible

The old attach() and launch() methods are now private helpers; connect()
is the only public entry point.

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import os
import sys
import time

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError

DEMO_PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_project", "DemoProject.rpyx")


def demo_attach_only() -> bool:
    """Demonstrate attaching to a running Rhapsody instance only.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 1: Attach to Running Instance (attach_only=True)")
    print("=" * 60)

    try:
        print("Attempting to attach to running Rhapsody instance...")
        app = RhapsodyApplication.connect(attach_only=True)
        print("[OK] Successfully attached to Rhapsody!")

        # Display application information
        print("\nApplication Information:")

        # Get active project if available
        try:
            active_project = app.activeProject()
            if active_project and active_project._com:
                print(f"  - Active project: {active_project.getName()}")
            else:
                print("  - Active project: None")
        except Exception as e:
            print(f"  - Active project: Unable to determine ({e})")

        # Clean up
        print("\nDisconnecting from Rhapsody...")
        app.disconnect()
        print("[OK] Disconnected successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"[-] Failed to attach: {e}")
        print("  Hint: Make sure Rhapsody is running before using this mode")
        return False


def demo_launch_new() -> bool:
    """Demonstrate launching a new Rhapsody instance.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 2: Launch New Instance (connect())")
    print("=" * 60)

    try:
        print("Attempting to launch new Rhapsody instance...")
        app = RhapsodyApplication.connect()
        print("[OK] Successfully launched Rhapsody!")

        app.openProject(DEMO_PROJECT_PATH)

        # Display application information
        print("\nApplication Information:")
        print(f"  - Project: {app.activeProject().getName()}")

        # Clean up
        print("\nClosing Rhapsody...")
        app.disconnect()
        print("[OK] Rhapsody closed successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"[-] Failed to launch: {e}")
        print("  Hint: Ensure Rhapsody is properly installed and licensed")
        return False


def demo_smart_connect() -> bool:
    """Demonstrate smart connection (attach with fallback to launch).

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 3: Smart Connection (Recommended)")
    print("=" * 60)

    try:
        print("Attempting smart connection (attach -> launch fallback)...")
        app = RhapsodyApplication.connect()
        print("[OK] Successfully connected to Rhapsody!")

        # Determine if we attached or launched
        try:
            # Try to get active project - this helps us understand the state
            active_project = app.activeProject()
            has_active_project = bool(active_project and active_project._com)
            connection_method = "attach" if has_active_project else "launch"
            print(f"\nConnection method used: {connection_method}")

            if has_active_project:
                print(f"  - Active project: {active_project.getName()}")
            else:
                # A freshly launched instance has no active project yet;
                # open the demo project so the rest of the demo has one.
                print("  - Active project: None (new instance launched)")
                active_project = app.openProject(DEMO_PROJECT_PATH)

        except Exception as e:
            print(f"  - Unable to determine connection method: {e}")
            active_project = None

        # Display application information
        print("\nApplication Information:")
        if active_project and active_project._com:
            print(f"  - Project: {active_project.getName()}")

        # Clean up
        print("\nDisconnecting from Rhapsody...")
        app.disconnect()
        print("[OK] Disconnected successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"[-] Failed to connect: {e}")
        print("  Hint: Ensure Rhapsody is properly installed and licensed")
        return False


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Basic Rhapsody Connection Methods")
    print("=" * 60)
    print("\nThis demo demonstrates three ways to connect to Rhapsody:")
    print("1. connect(attach_only=True) - Attach to running instance only")
    print("2. connect() - Launch new instance (with GUI)")
    print("3. connect() - Smart connection (recommended)")

    results = {}
    results["attach_only"] = demo_attach_only()
    results["launch"] = demo_launch_new()
    # Give the previous instance's process a moment to fully terminate
    # after disconnect() before the next method tries to attach/launch again.
    time.sleep(2)
    results["smart"] = demo_smart_connect()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for method, success in results.items():
        status = "[OK] Success" if success else "[-] Failed"
        print(f"{method:12} : {status}")

    successful = sum(results.values())
    total = len(results)
    print(f"\nTotal: {successful}/{total} methods successful")

    if successful == 0:
        print("\n[!] No connection methods worked.")
        print("  Please ensure:")
        print("  1. Rhapsody is properly installed")
        print("  2. You have a valid Rhapsody license")
        print("  3. You're running on Windows (COM API requirement)")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
