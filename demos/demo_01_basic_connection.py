#!/usr/bin/env python3
"""
Demo: Basic Rhapsody Connection Methods

This demo demonstrates the three different ways to connect to Rhapsody:
1. attach() - Connect to a running Rhapsody instance
2. launch() - Launch a new Rhapsody instance
3. connect() - Smart connection (tries attach first, falls back to launch)

Author: rhapsody-cli
Requirements: Windows with IBM Rhapsody installation
"""

import sys

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError


def demo_attach() -> bool:
    """Demonstrate attaching to a running Rhapsody instance.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 1: Attaching to Running Rhapsody Instance")
    print("=" * 60)

    try:
        print("Attempting to attach to running Rhapsody instance...")
        app = RhapsodyApplication.attach()
        print("✓ Successfully attached to Rhapsody!")

        # Display application information
        print("\nApplication Information:")
        # print(f"  - Version: {app.getVersion()}")  # type: ignore[attr-defined]
        # print(f"  - Install path: {app.getRhapsodyDir()}")  # type: ignore[attr-defined]

        # Get active project if available
        try:
            active_project = app.activeProject()
            if active_project:
                print(f"  - Active project: {active_project.getName()}")
            else:
                print("  - Active project: None")
        except Exception as e:
            print(f"  - Active project: Unable to determine ({e})")

        # Clean up
        print("\nDisconnecting from Rhapsody...")
        app.quit() 
        print("✓ Disconnected successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"✗ Failed to attach: {e}")
        print("  Hint: Make sure Rhapsody is running before using attach()")
        return False


def demo_launch() -> bool:
    """Demonstrate launching a new Rhapsody instance.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 2: Launching New Rhapsody Instance")
    print("=" * 60)

    try:
        print("Attempting to launch new Rhapsody instance...")
        app = RhapsodyApplication.launch()
        print("✓ Successfully launched Rhapsody!")

        app.openProject("C:\\Path\\To\\Your\\Project.rpy")  # Replace with a valid project path

        # Display application information
        print("\nApplication Information:")
        print(f"  - Project: {app.activeProject().getName()}")

        # Clean up
        print("\nClosing Rhapsody...")
        app.quit()
        print("✓ Rhapsody closed successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"✗ Failed to launch: {e}")
        print("  Hint: Ensure Rhapsody is properly installed and licensed")
        return False


def demo_connect() -> bool:
    """Demonstrate smart connection (attach with fallback to launch).

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 60)
    print("Method 3: Smart Connection (Recommended)")
    print("=" * 60)

    try:
        print("Attempting smart connection (attach → launch fallback)...")
        app = RhapsodyApplication.connect(prefer_attach=True)
        print("✓ Successfully connected to Rhapsody!")

        # Determine if we attached or launched
        try:
            # Try to get active project - this helps us understand the state
            active_project = app.activeProject()
            connection_method = "attach" if active_project else "launch"
            print(f"\nConnection method used: {connection_method}")

            if active_project:
                print(f"  - Active project: {active_project.getName()}")
            else:
                print("  - Active project: None (new instance launched)")

        except Exception as e:
            print(f"  - Unable to determine connection method: {e}")

        # Display application information
        print("\nApplication Information:")
        print(f"  - Project: {app.activeProject().getName()}")

        # Clean up
        print("\nDisconnecting from Rhapsody...")
        app.quit()
        print("✓ Disconnected successfully")

        return True

    except RhapsodyConnectionError as e:
        print(f"✗ Failed to connect: {e}")
        print("  Hint: Ensure Rhapsody is properly installed and licensed")
        return False


def main() -> None:
    """Main demo function."""
    print("=" * 60)
    print("Demo: Basic Rhapsody Connection Methods")
    print("=" * 60)
    print("\nThis demo demonstrates three ways to connect to Rhapsody:")
    print("1. attach() - Connect to running instance")
    print("2. launch() - Launch new instance")
    print("3. connect() - Smart connection (recommended)")

    results = {}
    # results["attach"] = demo_attach()
    results["launch"] = demo_launch()
    # results["connect"] = demo_connect()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for method, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"{method:12} : {status}")

    successful = sum(results.values())
    total = len(results)
    print(f"\nTotal: {successful}/{total} methods successful")

    if successful == 0:
        print("\n⚠ No connection methods worked.")
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
