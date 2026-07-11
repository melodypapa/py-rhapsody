# Rhapsody CLI Demo Scripts

This directory contains standalone demo scripts that demonstrate how to work with the IBM Rhapsody COM API using the rhapsody-cli package.

## Overview

All demo scripts now use a **persistent `demo_project/`** that ships with the package. This project contains a pre-seeded model (Domain::User class, Services::UserService, UseCases package with Customer actor and ManageUsers use case) for consistent, reproducible demonstrations.

**Key changes**:
- ✓ No need to prepare test projects manually
- ✓ Demos are **idempotent**: safe to run multiple times (demo_04 creates & cleans up elements)
- ✓ All demos use `DemoProject.rpyx` automatically
- ✓ Requires no interactive setup or pre-existing Rhapsody project

## Requirements

- **Operating System**: Windows (Rhapsody COM API is Windows-only)
- **Software**: IBM Rhapsody installation with valid license
- **Python**: 3.8 or higher
- **Package**: rhapsody-cli installed (`pip install rhapsody-cli`)

## Running the Demos

Each demo script can be run standalone:

```bash
python demos/demo_01_basic_connection.py
python demos/demo_02_project_operations.py
python demos/demo_03_element_navigation.py
python demos/demo_04_basic_element_creation.py
python demos/demo_05_error_handling.py
```

Or all in sequence:
```bash
for demo in demos/demo_0*.py; do python "$demo"; done
```

## Demo Scripts

### 1. demo_01_basic_connection.py
**Demonstrates**: Rhapsody connection methods and basic setup
- `attach()` - Connect to running Rhapsody instance
- `launch()` - Launch new Rhapsody instance
- `connect()` - Smart connection (attach with fallback to launch)
- Error handling for connection failures
- Proper application cleanup with `quit()`

**Output**: Shows three connection methods and success/failure for each

### 2. demo_02_project_operations.py
**Demonstrates**: Project management operations
- Opening `demo_project/DemoProject.rpyx` with `openProject()`
- Creating temporary scratch projects in `demo_project/_scratch_*/`
- Full project lifecycle (create → close → reopen)
- Automatic cleanup of scratch projects after demo
- Leaves shipped `DemoProject.rpyx` clean for subsequent runs

**Output**: Creates & destroys temporary test projects, verifies clean state

### 3. demo_03_element_navigation.py
**Demonstrates**: Element navigation and querying on the seeded model
- Navigating package structure with `getPackages()`, `getClasses()`
- Querying elements with `getNestedElementsByMetaClass()`
- Finding specific elements with `findNestedElementRecursive()`
- Displaying element properties (name, type, GUID, full path)
- Collection iteration & slicing patterns

**Model in demo_project**:
```
- Default (package)
- Domain::User (class with getId, getName, isActive operations)
- Services::UserService (class with findUser operation)
- UseCases
  - Customer (actor)
  - ManageUsers (use case)
```

### 4. demo_04_basic_element_creation.py
**Demonstrates**: Creating and cleaning up model elements
- Creating packages with `addPackage()`
- Creating classes with `addClass()`
- Adding attributes with `addAttribute()` and `setTypeDeclaration()`
- Adding operations with `addOperation()` and parameters with `addArgument()`
- Setting element properties (name, description, visibility)
- **Cleanup**: Deletes all created elements via `deleteFromProject()` before save
- Verifies `demo_project` remains clean after execution

**Idempotency**: Safe to run multiple times - created elements are cleaned up automatically

### 5. demo_05_error_handling.py
**Demonstrates**: Error handling patterns and recovery
- Connection error handling (attach vs. launch fallback)
- Project operation error handling
- Element not found scenarios (gracefully returns empty wrapper)
- COM error translation to `RhapsodyRuntimeException`
- Safe element iteration patterns
- Proper cleanup in finally blocks

**Scenarios**: Shows intentional errors and demonstrates proper error catching/handling

## The demo_project

Located in `demos/demo_project/`, contains:
- **DemoProject.rpyx** - Rhapsody project file (committed to git)
- **DemoProject_rpy/** - Rhapsody internal structure (XML component files)
- **_scratch_*/** - Temporary scratch projects created by demo_02 (auto-cleaned, .gitignored)

**Regenerating demo_project** (if needed):
```bash
python demos/_bootstrap_demo_project.py
```
This script uses the rhapsody-cli API to programmatically create the seeded model.

## Key Patterns Used in Demos

### Proper Connection & Cleanup
```python
from rhapsody_cli.application import RhapsodyApplication

app = RhapsodyApplication.connect()  # attach() with fallback to launch()
try:
    # Your code here
finally:
    app.quit()  # Always cleanup, use quit() not disconnect()
    time.sleep(2)  # Allow COM lifecycle to settle
```

### Safe Element Access
```python
# Check _com attribute to detect "not found" results
element = project.findNestedElement("Name", "Class")
if element and element._com:
    print(element.getName())
else:
    print("Element not found")
```

### Type Declarations
```python
attr = cls.addAttribute("id")
attr.setTypeDeclaration("int")  # Not setType() - use type strings

op = cls.addOperation("getId")
op.setReturnTypeDeclaration("int")
arg = op.addArgument("count")  # Not addParameter()
arg.setTypeDeclaration("int")
```

## Expected Output

Each demo script provides clear console output showing:
- What operation is being performed (`[OK]` for success, `[-]` for failure)
- Intermediate results and element information
- Any errors encountered and how they're handled
- Final status and cleanup messages

Example:
```
[OK] Connected successfully
[OK] Active project: DemoProject
  - Name: User
  - Type: Class
  - GUID: GUID cb0f10f4-70bb-4e28-95d4-2b01128199cc
  - Full path name: Domain::User
```

## Troubleshooting

### "No running Rhapsody instance found"
- **Solution**: This is expected - demos use `launch()` fallback automatically
- **Check**: Ensure Rhapsody is properly installed and licensed

### "Cannot open demo_project" or file not found
- **Solution**: Verify rhapsody-cli is installed in the current environment
- **Check**: `demos/demo_project/DemoProject.rpyx` exists

### "COM error" or "RhapsodyRuntimeException"
- **Solution**: Ensure Rhapsody is properly installed and licensed
- **Check**: Rhapsody version compatibility with your Python environment
- **Note**: Some operations may fail if Rhapsody internals change

### Demo runs but doesn't complete
- **Solution**: Demos can take 30+ seconds due to COM initialization
- **Try**: Run with explicit timeout: `timeout 120 python demos/demo_03_element_navigation.py`

### Permission errors
- **Solution**: Run terminal/command prompt as Administrator
- **Check**: Folder permissions for Windows COM API access

## Tips for Best Results

1. **Start with demo_01**: Verify connection works first
2. **Run demo_02 second**: Confirms project operations
3. **Run demo_03 third**: Tests navigation on seeded model
4. **Run demo_04**: Tests creation & cleanup (safe to run multiple times)
5. **Run demo_05 last**: Tests error handling
6. **Review output**: Each demo shows what it's doing - follow along

## Advanced: Running Demos Programmatically

You can import demos programmatically (though not recommended - run as scripts instead):

```python
import sys
sys.path.insert(0, '/path/to/rhapsody-cli')

# Direct execution via subprocess is safer
import subprocess
result = subprocess.run([sys.executable, 'demos/demo_03_element_navigation.py'])
```

## Additional Resources

- **API Documentation**: `docs/api/` - Complete API reference
- **User Guides**: `docs/user_guide/` - Step-by-step tutorials
- **Requirements Specs**: `docs/requirements/` - What features are specified
- **Project README**: Root `README.md` - Installation and architecture

## Support

For issues with the demos:
1. Check that rhapsody-cli is properly installed
2. Verify Rhapsody installation and license
3. Review the error messages - they often indicate the root cause
4. Check the main project README.md for broader troubleshooting

