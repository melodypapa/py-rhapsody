# rhapsody-cli

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/user/rhapsody-cli)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A Pythonic, object-oriented wrapper around the IBM Rhapsody COM API for
Windows. Method names and class hierarchy mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge and documentation transfer directly.

## Features

- **Complete API Mirroring**: Method names and signatures match the Rhapsody Java API exactly (converted to snake_case)
- **Object-Oriented Design**: Clean Python classes wrapping COM objects with proper type hints
- **Comprehensive Element Support**: 96 Rhapsody element types wrapped with full method coverage
- **CLI Tools**: Command-line utilities for project, package, class, operation, attribute, port, export, and import management
- **Multi-Level Path Navigation**: Navigate hierarchical model structures using `/` or `\` separators
- **Bulk Operations**: Create multiple elements, list recursively, and delete with safety confirmations
- **Robust Error Handling**: Automatic COM error translation with user-friendly exception messages
- **Mocked Testing**: Full test suite runs without Rhapsody installation or license
- **Type Safety**: Strict mypy checking with comprehensive type annotations
- **Cross-Instance Support**: Manage multiple simultaneous Rhapsody instances in the same process

## Requirements

- Windows with a licensed IBM Rhapsody installation (COM automation is
  Windows-only)
- Python 3.8+
- `pywin32` (automatically installed on Windows)

## Installation

### Basic Installation

```bash
pip install rhapsody-cli
```

### Development Installation

```bash
pip install -e ".[dev,cli]"
```

This installs:
- **Core dependencies**: `pywin32` (Windows COM support)
- **CLI dependencies**: `tabulate`, `rich` (table formatting and colored output)
- **Dev dependencies**: `pytest`, `pytest-cov`, `ruff`, `black`, `mypy` (testing and linting)

## Usage

### Python API

```python
from rhapsody_cli import RhapsodyApplication

# Attaches to a running Rhapsody instance, or launches a new one if none
# is running.
app = RhapsodyApplication.connect()

# Open an existing project
project = app.open_project(r"C:\Models\MyProject.rpy")

# Create a new package
package = project.add_package("Sensors")

# Add classes with attributes and operations
sensor_class = package.add_class("TemperatureSensor")
sensor_class.add_attribute("currentTemperature")
sensor_class.add_operation("readTemperature")

# Navigate existing elements
for cls in project.get_nested_elements_by_meta_class("Class", 1):  # recursive
    print(f"Class: {cls.get_name()}")
    for attr in cls.get_attributes():
        print(f"  Attribute: {attr.get_name()}")

# Save and quit
project.save()
app.quit()
```

### Command-Line Interface

The CLI provides eight command groups: `project`, `package`, `class`, `attribute`, `operation`, `port`, `export`, and `import`.

#### Project Management

```bash
# Create a new project
rhapsody-cli project new "C:\Models" NewProject

# Open an existing project
rhapsody-cli project open "C:\Models\MyProject.rpy"

# List open projects / close the active project
rhapsody-cli project list
rhapsody-cli project close
```

#### Package Management

```bash
# Create a package (omit --path for a root package)
rhapsody-cli package create --path Sensors '{"name":"Actuators"}'

# View / list packages (supports table, json, csv output)
rhapsody-cli package view --path Sensors/Actuators --format json
rhapsody-cli package list --path Sensors --format table

# Update or delete a package
rhapsody-cli package update --path Sensors/Actuators '{"description":"Updated"}'
rhapsody-cli package delete --path Sensors/Actuators
```

#### Class Management

```bash
rhapsody-cli class create --path Sensors '{"name":"TemperatureSensor"}'
rhapsody-cli class view --path Sensors/TemperatureSensor --format json
rhapsody-cli class list --path Sensors
rhapsody-cli class link --path Sensors/TemperatureSensor --add BaseSensor
rhapsody-cli class update --path Sensors/TemperatureSensor '{"isAbstract":true}'
rhapsody-cli class delete --path Sensors/TemperatureSensor
```

#### Attribute, Operation, and Port Management

`attribute`, `operation`, and `port` share the same argument shape (`--path` to the owning classifier, `--name` or `--guid` to identify the member, and an inline/`--input` JSON payload):

```bash
rhapsody-cli attribute create --path Sensors/TemperatureSensor '{"name":"threshold","type":"int"}'
rhapsody-cli operation create --path Sensors/TemperatureSensor '{"name":"readValue"}'
rhapsody-cli port create --path Sensors/TemperatureSensor '{"name":"clientPort"}'

rhapsody-cli attribute list --path Sensors/TemperatureSensor
rhapsody-cli attribute update --path Sensors/TemperatureSensor --name threshold '{"isStatic":true}'
rhapsody-cli attribute delete --path Sensors/TemperatureSensor --name threshold
```

#### Export and Import (YAML)

The `export` and `import` command groups serialize Rhapsody model elements to / from YAML:

```bash
# Export a project or package to a YAML file
rhapsody-cli export project --path MyProject "C:\Models\MyProject.yaml"
rhapsody-cli export package --path Sensors "C:\Models\Sensors.yaml"

# Import a previously exported YAML file back into Rhapsody
rhapsody-cli import project "C:\Models\MyProject.yaml"
rhapsody-cli import package "C:\Models\Sensors.yaml"
```

### Global Options

`--verbose`/`-v` and `--format {table,json,csv}` are specified **after** the command group name (most subcommands also accept a per-action `--output <file>`):

```bash
# Enable verbose logging
rhapsody-cli class list --path Sensors --verbose

# Specify output format
rhapsody-cli package view --path Sensors --format json
```

### Multi-Instance Support

```python
from rhapsody_cli import RhapsodyApplication

# Manage multiple simultaneous Rhapsody instances via connect()
# (attach()/launch() are internal; connect() is the public entry point)
app1 = RhapsodyApplication.connect(attach_only=True)  # Attach to a running instance
app2 = RhapsodyApplication.connect()                  # Attach, or launch a new one if none running

project1 = app1.open_project("project1.rpy")
project2 = app2.open_project("project2.rpy")

# Each instance operates independently
```

## Development

### Running Tests

```bash
# Run all unit tests (1621 tests, no Rhapsody installation required)
pytest tests/unit

# Run with coverage
pytest --cov=rhapsody_cli --cov-report=html

# Run integration tests (requires running Rhapsody with open project)
pytest tests/integration
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/ tests/

# All checks in one
pytest && ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/
```

### Test Coverage

- **1621 unit tests** covering all wrapped methods and edge cases
- **Mocked COM objects** (`tests/unit/models/fakes.py`) - no Rhapsody installation required
- **Integration tests** for real COM automation verification
- **Branch coverage** tracking with 80% minimum threshold

## Architecture

### Core Design

The package follows a systematic wrapping pattern:

1. **Connection Layer**: `RhapsodyApplication` manages COM connections
2. **Wrapping Pattern**: Each wrapper stores `_com` and delegates all calls
3. **Type Registry**: Central registry maps Rhapsody types to Python wrappers
4. **Automatic Fallback**: Unknown types fall back to generic `RPModelElement`
5. **Collection Wrapping**: `RPCollection` provides Pythonic iteration

### Class Hierarchy

Mirrors the Rhapsody Java API hierarchy:

```
RPModelElement (wraps IRPModelElement - base for all model elements)
└─ RPUnit (wraps IRPUnit - elements that can be saved as files)
   ├─ RPProject (wraps IRPProject)
   ├─ RPPackage (wraps IRPPackage)
   ├─ RPClassifier (wraps IRPClassifier)
   │  ├─ RPClass (wraps IRPClass)
   │  ├─ RPActor (wraps IRPActor)
   │  ├─ RPUseCase (wraps IRPUseCase)
   │  └─ ... (15+ classifier types)
   └─ ... (96 total wrapped element types)
```

### Adding New Element Types

Supporting new Rhapsody element types is mechanical:

1. Define a wrapper class inheriting from the appropriate base
2. Implement methods delegating to `self._com`
3. Register in the type registry with `register_wrapper()`
4. Add unit tests following the established pattern

## Documentation

### Building Documentation Locally

The project uses **Sphinx** with the **ReadTheDocs theme** to generate comprehensive documentation including API reference, user guides, and examples.

#### Install Documentation Dependencies

```bash
pip install -r docs/requirements.txt
```

This installs:
- `sphinx>=4.0.0` - Documentation generator
- `sphinx-rtd-theme>=1.0.0` - ReadTheDocs theme
- `myst-parser>=0.18.0` - Markdown support for Sphinx

#### Generate HTML Documentation

```bash
# Navigate to docs directory
cd docs

# Build HTML documentation
make html

# On Windows (PowerShell)
.\make.bat html
```

The generated documentation will be in `docs/_build/html/`.

#### View Documentation Locally

```bash
# Open the main documentation page
start docs/_build/html/index.html        # Windows
open docs/_build/html/index.html         # macOS
xdg-open docs/_build/html/index.html     # Linux
```

#### Alternative Build Formats

```bash
# Build PDF documentation (requires LaTeX)
make latexpdf

# Build coverage report (checks documentation coverage)
make coverage

# View all available build formats
make help
```

#### Documentation Structure

- **Design Document**: `docs/superpowers/specs/2026-07-06-rhapsody-cli-com-api-design.md`
- **API Reference**: `docs/api/` - auto-generated from docstrings using Sphinx autodoc
- **User Guide**: `docs/user_guide/` - comprehensive usage tutorials
- **Examples**: `docs/examples/` - advanced workflow examples
- **Code Guidelines**: `docs/CODE_GUIDELINES.md` - development standards

#### Deploying to ReadTheDocs

To deploy documentation to [ReadTheDocs.io](https://readthedocs.io):

1. **Create ReadTheDocs Project**: Import your GitHub repository at https://readthedocs.io
2. **Configure Build Settings**:
   - Python interpreter: Python 3.x
   - Requirements file: `docs/requirements.txt`
   - Configuration file: `docs/conf.py`
3. **Enable Auto-Build**: ReadTheDocs automatically rebuilds on every push to main branch
4. **Access Online Docs**: Your documentation will be available at `https://rhapsody-cli.readthedocs.io`

#### Sphinx Configuration Features

The `docs/conf.py` configuration includes:
- **Autodoc extension**: Automatically generates API docs from Python docstrings
- **Napoleon extension**: Parses Google-style and NumPy-style docstrings
- **Myst parser**: Enables Markdown support alongside reStructuredText
- **Intersphinx**: Links to Python standard library documentation
- **Coverage checking**: Validates all modules are documented
- **Type hints**: Displays type annotations in documentation

## Supported Rhapsody Elements

The package currently wraps **96 element types** including:

**Containment Elements**: Project, Package, Profile, Module, Configuration, Node, Component, ComponentInstance, Collaboration

**Classifier Elements**: Class, Actor, UseCase, InterfaceItem, Stereotype, Statechart, Operation, AssociationClass

**Relation Elements**: Relation, Instance, Dependency, Generalization, Hyperlink, AssociationRole

**Leaf Elements**: Attribute, Tag, Requirement, Variable, Annotation, Constraint, EnumerationLiteral, Diagram, Comment

Plus **hundreds of generic methods** from `RPModelElement` available on all element types.

## Contributing

See [Contributing Guide](docs/contributing.rst) for:

- Code style guidelines
- Test requirements
- Documentation standards
- Pull request process

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### v0.2.0 (2026-07-20)

- **Breaking**: Renamed all wrapper methods from camelCase to snake_case (`addClass` → `add_class`, `getName` → `get_name`, etc.) for consistent Pythonic naming
- **Breaking**: Removed the generic `element` and `io` command groups in favor of dedicated per-type commands
- Added `package`, `class`, `operation`, `attribute`, and `port` command groups, each with `create`/`list`/`view`/`delete` subcommands (plus `update` for `package` and `class`, and `link` for `class` generalization)
- Added `RPPort` wrapper and `RPClassifier.add_port()` convenience method
- Added `export` and `import` command groups with `project`/`package` subcommands for YAML-based model exchange (RhapsodyExporter / RhapsodyImporter)
- Expanded wrapped element coverage from 50+ to **96** element types
- Enhanced package duplicate detection with clearer, user-friendly error messages
- Refactored CLI error handling to use logger + `CliExecutionError` instead of `print()`/`sys.exit()`
- Various Sphinx documentation and build-warning fixes

### v0.1.0 (2026-07-09)

- Initial release with 50+ wrapped Rhapsody element types
- Complete CLI tools for element, project, and I/O operations
- Multi-level path navigation with `/` and `\` separator support
- Comprehensive test suite (554 unit tests) with mocked COM objects
- Strict type checking with mypy
- Sphinx documentation with API reference and user guides

## Limitations

- **Windows-only**: Rhapsody COM automation is Windows-only
- **Requires Rhapsody License**: Actual COM calls require licensed Rhapsody installation
- **Not all 160+ interfaces**: Core ~50 types wrapped; others fall back to generic wrapper
- **No Design Manager**: Deprecated Design Manager features not supported

## Comparison with Rhapsody Java API

| Aspect | Java API | rhapsody-cli |
|--------|----------|--------------|
| Method Names | `getName()` | `get_name()` ✓ |
| Class Hierarchy | `IRPClass extends IRPClassifier` | `RPClass(RPClassifier)` ✓ |
| Collections | `IRPCollection` | `RPCollection` ✓ |
| Error Handling | COM errors | `RhapsodyRuntimeException` ✓ |
| Type Safety | Checked at compile | mypy strict mode ✓ |
| Testing | Requires Rhapsody | Mocked COM objects ✓ |

## Support

- **Issues**: GitHub Issues for bug reports and feature requests
- **Documentation**: Full API docs at `docs/api/` and user guide at `docs/user_guide/`
- **Examples**: Advanced usage patterns in `docs/examples/`