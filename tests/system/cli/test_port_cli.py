"""System tests for the `port` CLI command group.

Tests port CRUD lifecycle via subprocess against a live Rhapsody project.

Path notes: Paths use "/" separator. Port view/delete require TWO
args: --path <class_path> AND --name <port_name> (or --guid). They do NOT
accept a combined element path.
"""

import json
import uuid

import pytest

from tests.system.cli.conftest import _run_cli, _unique_name


@pytest.mark.system
class TestPortCLI:
    """Test port CLI commands via subprocess."""

    @pytest.fixture(autouse=True)
    def _require_rhapsody(self, _require_rhapsody: None) -> None:
        """Skip these tests if no Rhapsody instance is available."""

    @staticmethod
    def _create_package_and_class(pkg_name: str, cls_name: str) -> tuple[str, str]:
        """Create a package at root and a class under it.

        Returns:
            Tuple of (pkg_path, cls_path). Both use "/" separator.
        """
        pkg_json = json.dumps({"name": pkg_name})
        result = _run_cli("package", "create", "--input", pkg_json)
        assert result.returncode == 0, f"Failed to create package: {result.stderr}"
        pkg_path = pkg_name

        cls_json = json.dumps({"name": cls_name})
        result = _run_cli("class", "create", "--path", pkg_path, "--input", cls_json)
        assert result.returncode == 0, f"Failed to create class: {result.stderr}"
        cls_path = f"{pkg_path}/{cls_name}"
        return pkg_path, cls_path

    def test_port_create_under_class(self, cli_project: str) -> None:
        """Test creating a port under a class."""
        pkg_name = _unique_name("PortPkg")
        cls_name = _unique_name("PortCls")
        port_name = _unique_name("myPort")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            port_json = json.dumps({"name": port_name})
            result = _run_cli("port", "create", "--path", cls_path, "--input", port_json)
            assert result.returncode == 0, f"Failed: {result.stderr}"

            # Verify via list
            list_result = _run_cli("port", "list", "--path", cls_path, "--format", "json")
            assert list_result.returncode == 0
            ports = json.loads(list_result.stdout)
            assert port_name in ports
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_view_existing(self, cli_project: str) -> None:
        """Test viewing an existing port via --path + --name."""
        pkg_name = _unique_name("ViewPkg")
        cls_name = _unique_name("ViewCls")
        port_name = _unique_name("viewPort")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            port_json = json.dumps({"name": port_name})
            _run_cli("port", "create", "--path", cls_path, "--input", port_json)

            # View uses --path <class_path> --name <port_name> (NOT a combined path)
            result = _run_cli("port", "view", "--path", cls_path, "--name", port_name, "--format", "json")
            assert result.returncode == 0, f"Failed: {result.stderr}"
            data = json.loads(result.stdout)
            assert data["name"] == port_name
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_view_nonexistent(self, cli_project: str) -> None:
        """Test viewing a non-existent port returns error."""
        pkg_name = _unique_name("NoPortPkg")
        cls_name = _unique_name("NoPortCls")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            # View uses --path + --name (not a combined path)
            result = _run_cli(
                "port", "view",
                "--path", cls_path,
                "--name", f"NonExistent_{uuid.uuid4().hex[:8]}",
            )
            assert result.returncode != 0
            assert "error" in result.stderr.lower() or "failed" in result.stderr.lower()
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_list_in_class(self, cli_project: str) -> None:
        """Test listing ports in a class."""
        pkg_name = _unique_name("ListPkg")
        cls_name = _unique_name("ListCls")
        port1_name = _unique_name("port1")
        port2_name = _unique_name("port2")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            _run_cli("port", "create", "--path", cls_path, "--input", json.dumps({"name": port1_name}))
            _run_cli("port", "create", "--path", cls_path, "--input", json.dumps({"name": port2_name}))

            result = _run_cli("port", "list", "--path", cls_path, "--format", "json")
            assert result.returncode == 0
            ports = json.loads(result.stdout)
            assert port1_name in ports
            assert port2_name in ports
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_delete_existing(self, cli_project: str) -> None:
        """Test deleting an existing port via --path + --name."""
        pkg_name = _unique_name("DelPkg")
        cls_name = _unique_name("DelCls")
        port_name = _unique_name("delPort")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            _run_cli("port", "create", "--path", cls_path, "--input", json.dumps({"name": port_name}))

            # Delete uses --path <class_path> --name <port_name> (NOT a combined path)
            result = _run_cli("port", "delete", "--path", cls_path, "--name", port_name)
            assert result.returncode == 0, f"Failed: {result.stderr}"

            # Verify port is gone
            list_result = _run_cli("port", "list", "--path", cls_path, "--format", "json")
            assert list_result.returncode == 0
            ports = json.loads(list_result.stdout)
            assert port_name not in ports
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_delete_nonexistent(self, cli_project: str) -> None:
        """Test deleting a non-existent port returns error."""
        pkg_name = _unique_name("NoDelPkg")
        cls_name = _unique_name("NoDelCls")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            # Delete uses --path + --name
            result = _run_cli(
                "port", "delete",
                "--path", cls_path,
                "--name", f"NonExistent_{uuid.uuid4().hex[:8]}",
            )
            assert result.returncode != 0
            assert "error" in result.stderr.lower() or "failed" in result.stderr.lower()
        finally:
            _run_cli("package", "delete", "--path", pkg_path)

    def test_port_create_invalid_json(self, cli_project: str) -> None:
        """Test that invalid JSON input returns error."""
        pkg_name = _unique_name("BadJsonPkg")
        cls_name = _unique_name("BadJsonCls")
        pkg_path, cls_path = self._create_package_and_class(pkg_name, cls_name)

        try:
            result = _run_cli("port", "create", "--path", cls_path, "--input", "{invalid}")
            assert result.returncode != 0
            assert "json" in result.stderr.lower() or "error" in result.stderr.lower()
        finally:
            _run_cli("package", "delete", "--path", pkg_path)
