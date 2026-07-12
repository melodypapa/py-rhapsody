# rhapsody-cli

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/user/rhapsody-cli)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A Pythonic, object-oriented wrapper around the IBM Rhapsody COM API for
Windows. Method names and class hierarchy mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge and documentation transfer directly.

## Features

- **Complete API Mirroring**: Method names and signatures match the Rhapsody Java API exactly
- **Object-Oriented Design**: Clean Python classes wrapping COM objects with proper type hints
- **Comprehensive Element Support**: 50+ Rhapsody element types wrapped with full method coverage
- **CLI Tools**: Command-line utilities for element management, I/O operations, and project handling
- **Multi-Level Path Navigation**: Navigate hierarchical model structures using `/` or `\` separators
- **Bulk Operations**: Add multiple elements, query recursively, and delete with safety confirmations
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
package = project.addPackage("Sensors")

# Add classes with attributes and operations
sensor_class = package.addClass("TemperatureSensor")
sensor_class.addAttribute("currentTemperature")
sensor_class.addOperation("readTemperature")

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

The CLI provides three main command groups:

#### Element Management

```bash
# Add elements with multi-level paths
rhapsody-cli element add --type class --path "Sensors/TemperatureSensor"
rhapsody-cli element add --type actor --path "System/User" --name "AdminUser"

# View element details (supports JSON, CSV, table output)
rhapsody-cli element view --path "Sensors/TemperatureSensor" --output json

# Query elements with pattern matching
rhapsody-cli element query "Sensor*" --output table
rhapsody-cli element query --path "Sensors" --recursive

# Delete elements with safety confirmation
rhapsody-cli element delete "Sensors/OldSensor"
```

#### Project Management

```bash
# Create a new project
rhapsody-cli project create --location "C:\Models" --name "NewProject"

# Open existing project
rhapsody-cli project open --file "C:\Models\MyProject.rpy"

# Attach to active project in running Rhapsody
rhapsody-cli project attach
```

#### I/O Operations

```bash
# Export model to various formats
rhapsody-cli io export --format json --output model.json

# Import model data
rhapsody-cli io import --file import_data.json
```

### Global Options

```bash
# Enable verbose logging
rhapsody-cli --verbose element query

# Specify output format
rhapsody-cli --output json element view --path " MyClass"
```

### Multi-Instance Support

```python
from rhapsody_cli import RhapsodyApplication

# Manage multiple simultaneous Rhapsody instances
app1 = RhapsodyApplication.attach()  # Attach to first instance
app2 = RhapsodyApplication.launch()  # Launch second instance

project1 = app1.open_project("project1.rpy")
project2 = app2.open_project("project2.rpy")

# Each instance operates independently
```

## Development

### Running Tests

```bash
# Run all unit tests (554 tests, no Rhapsody installation required)
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

- **554 unit tests** covering all wrapped methods and edge cases
- **Mocked COM objects** (`tests/fakes.py`) - no Rhapsody installation required
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
   └─ ... (50+ total wrapped element types)
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

The package currently wraps **50+ element types** including:

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