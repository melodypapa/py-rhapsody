#!/usr/bin/env python3
"""
Bootstrap script: generates ``demos/demo_project``.

This is NOT one of the numbered demo scripts. It is a one-time (re)generation
utility that uses rhapsody-cli itself to create the small Rhapsody project
that the numbered demos (demo_01 .. demo_05) open and exercise for
verification purposes.

Run this script whenever ``demos/demo_project`` needs to be regenerated from
scratch (for example, after a Rhapsody upgrade changes the on-disk project
format). The generated files are committed to the repository, so running
this script is normally NOT required to use the demos.

Usage:
    python demos/_bootstrap_demo_project.py

Requirements: Windows with IBM Rhapsody installation.
"""

import os
import shutil
import sys

from rhapsody_cli.application import RhapsodyApplication

DEMO_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + "demo_project"
PROJECT_NAME = "DemoProject"


def _clean_demo_project_dir() -> None:
    """Remove any previously generated project files."""
    if os.path.isdir(DEMO_PROJECT_DIR):
        for entry in os.listdir(DEMO_PROJECT_DIR):
            full_path = os.path.join(DEMO_PROJECT_DIR, entry)
            if entry == ".gitkeep":
                continue
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
    else:
        os.makedirs(DEMO_PROJECT_DIR)


def build_demo_project() -> None:
    """Create and populate the demo_project used by the numbered demos."""
    print("Connecting to Rhapsody...")
    app = RhapsodyApplication.connect()

    try:
        print(f"Creating project '{PROJECT_NAME}' at {DEMO_PROJECT_DIR}...")
        project = app.create_new_project(DEMO_PROJECT_DIR, PROJECT_NAME)

        # --- Domain package: User class -------------------------------
        print("Creating package 'Domain'...")
        domain = project.add_package("Domain")
        domain.set_description("Core domain model for the rhapsody-cli demos.")

        print("Creating class 'Domain::User'...")
        user_class = domain.add_class("User")
        user_class.set_description("Represents a user in the system.")

        id_attr = user_class.add_attribute("id")
        id_attr.set_type_declaration("int")
        id_attr.set_default_value("0")
        id_attr.set_description("Unique identifier.")

        name_attr = user_class.add_attribute("name")
        name_attr.set_type_declaration("String")
        name_attr.set_description("Name of the user.")

        active_attr = user_class.add_attribute("active")
        active_attr.set_type_declaration("boolean")
        active_attr.set_default_value("true")
        active_attr.set_description("Active status flag.")

        get_id_op = user_class.add_operation("getId")
        get_id_op.set_return_type_declaration("int")
        get_id_op.set_description("Get the unique identifier.")

        get_name_op = user_class.add_operation("getName")
        get_name_op.set_return_type_declaration("String")
        get_name_op.set_description("Get the name of the user.")

        is_active_op = user_class.add_operation("isActive")
        is_active_op.set_return_type_declaration("boolean")
        is_active_op.set_description("Check if the user is active.")

        # --- Services package: UserService class ------------------------
        print("Creating package 'Services'...")
        services = project.add_package("Services")
        services.set_description("Service layer for the rhapsody-cli demos.")

        print("Creating class 'Services::UserService'...")
        user_service_class = services.add_class("UserService")
        user_service_class.set_description("Service for managing users.")

        find_user_op = user_service_class.add_operation("findUser")
        find_user_arg = find_user_op.add_argument("id")
        find_user_arg.set_type_declaration("int")
        find_user_op.set_return_type_declaration("User")
        find_user_op.set_description("Find a user by identifier.")

        # --- UseCases package: actor and use case ------------------------
        # Actors and use cases must live inside a package (adding them
        # directly at the project's top level is rejected by Rhapsody).
        print("Creating package 'UseCases'...")
        use_cases_pkg = project.add_package("UseCases")
        use_cases_pkg.set_description("Actors and use cases for the rhapsody-cli demos.")

        print("Creating actor 'Customer'...")
        customer_actor = use_cases_pkg.add_actor("Customer")
        customer_actor.set_description("A customer of the system.")

        print("Creating use case 'ManageUsers'...")
        manage_users_uc = use_cases_pkg.add_use_case("ManageUsers")
        manage_users_uc.set_description("Use case for managing users in the system.")

        print("Saving project...")
        project.save()

        print(f"\n[OK] Demo project created at: {project.get_filename()}")
    finally:
        print("Closing Rhapsody...")
        app.disconnect()


def main() -> None:
    """Main entry point."""
    print("=" * 60)
    print("Bootstrap: Generate demos/demo_project")
    print("=" * 60)

    _clean_demo_project_dir()
    build_demo_project()

    print("\n" + "=" * 60)
    print("Done. Review the generated files under demos/demo_project")
    print("and commit them to the repository.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - top-level bootstrap script
        print(f"[-] Failed to build demo project: {exc}")
        sys.exit(1)
