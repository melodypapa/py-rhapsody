# py_rhapsody

A Pythonic, object-oriented wrapper around the IBM Rhapsody COM API for
Windows. Method names and class hierarchy mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge and documentation transfer directly.

## Requirements

- Windows with a licensed IBM Rhapsody installation (COM automation is
  Windows-only).
- Python 3.8+
- `pywin32`

## Installation

```bash
pip install -e .[dev]
```

## Usage

```python
from py_rhapsody import RhapsodyApplication

# Attaches to a running Rhapsody instance, or launches a new one if none
# is running.
app = RhapsodyApplication.connect()

project = app.openProject(r"C:\Models\MyProject.rpy")
package = project.addPackage("Sensors")
sensor_class = package.addClass("TemperatureSensor")
sensor_class.addAttribute("currentTemperature")
sensor_class.addOperation("readTemperature")

project.save()
```

## Development

```bash
pip install -e .[dev]
pytest
ruff check src/ tests/
black --check src/ tests/
mypy src/ tests/
```

Tests run entirely against mocked COM objects (see `tests/fakes.py`) — no
Rhapsody installation or license is required to run the test suite.

## Design

See `docs/superpowers/specs/2026-07-06-py-rhapsody-com-api-design.md` for
the full architecture and design rationale.
