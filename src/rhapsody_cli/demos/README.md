# Rhapsody CLI Demo Scripts

This directory contains standalone demo scripts that demonstrate how to work with the IBM Rhapsody COM API using the rhapsody-cli package.

## Requirements

- **Operating System**: Windows (Rhapsody COM API is Windows-only)
- **Software**: IBM Rhapsody installation with valid license
- **Python**: 3.8 or higher
- **Package**: rhapsody-cli installed (`pip install rhapsody-cli`)

## Running the Demos

Each demo script can be run independently in two ways:

### Method 1: Direct execution
```bash
python src/rhapsody_cli/demos/demo_01_basic_connection.py
```

### Method 2: Module execution
```bash
python -m rhapsody_cli.demos.demo_01_basic_connection
```

## Demo Scripts

### 1. demo_01_basic_connection.py
**Demonstrates**: Rhapsody connection methods and basic setup
- `attach()` - Connect to running Rhapsody instance
- `launch()` - Launch new Rhapsody instance
- `connect()` - Smart connection (attach with fallback to launch)
- Error handling for connection failures
- Proper application cleanup

**Requirements**: Running Rhapsody instance recommended

### 2. demo_02_project_operations.py
**Demonstrates**: Project management operations
- Opening existing projects with `openProject()`
- Creating new projects with `createNewProject()`
- Getting active project with `activeProject()`
- Listing all open projects with `getProjects()`
- Saving and closing projects
- Error handling for missing files

**Requirements**: Existing .rpy file or permission to create new projects

### 3. demo_03_element_navigation.py
**Demonstrates**: Element navigation and querying
- Navigating package structure with `getPackages()`, `getClasses()`
- Querying elements with `getNestedElementsByMetaClass()`
- Finding specific elements with `findNestedElement()`
- Displaying element properties (name, type, GUID)
- Collection iteration patterns

**Requirements**: Open project with model elements

### 4. demo_04_basic_element_creation.py
**Demonstrates**: Creating model elements
- Creating packages with `addPackage()`
- Creating classes with `addClass()`
- Adding attributes to classes
- Adding operations to classes
- Setting element properties
- Saving and verifying creation

**Requirements**: Open project or permission to create new elements

### 5. demo_05_error_handling.py
**Demonstrates**: Error handling patterns
- Connection error handling
- Project operation error handling
- Element not found scenarios
- COM error translation
- Proper cleanup after errors

**Requirements**: None (demonstrates error scenarios)

## Expected Output

Each demo script provides clear console output showing:
- What operation is being performed
- Intermediate results and element information
- Any errors encountered and how they're handled
- Final status and cleanup messages

## Troubleshooting

### "No running Rhapsody instance found"
- **Solution**: Launch Rhapsody manually before running demos that use `attach()`
- **Alternative**: Use demos that call `launch()` or `connect()` instead

### "Cannot open project file"
- **Solution**: Verify the file path is correct and the .rpy file exists
- **Alternative**: Use `createNewProject()` to create a new project instead

### "COM error" or "RhapsodyRuntimeException"
- **Solution**: Ensure Rhapsody is properly installed and licensed
- **Check**: Rhapsody version compatibility with your Python environment

### Permission errors
- **Solution**: Run your terminal/command prompt as Administrator
- **Check**: Folder permissions for project creation/modification

## Programmatic Usage

You can also import and use these demos programmatically:

```python
from rhapsody_cli.demos import demo_connection, demo_projects

# Run connection demo
demo_connection()

# Run project operations demo
demo_projects()
```

## Tips for Best Results

1. **Start with demo_01**: Ensure basic connectivity works first
2. **Use existing project**: Start with demo_03 using an existing Rhapsody project
3. **Check permissions**: Ensure you have write permissions for project modifications
4. **Save work**: Some demos create/modify elements - save if you want to keep changes
5. **Review output**: Each demo shows what it's doing - follow along in the output

## Additional Resources

- **Sphinx Documentation**: `docs/examples/` - Comprehensive examples in RST format
- **API Reference**: `docs/api/` - Complete API documentation
- **User Guides**: `docs/user_guide/` - Step-by-step tutorials
- **README.md**: Project root - Installation and usage overview

## Support

For issues or questions about Rhapsody automation:
1. Check the main project README.md
2. Review Sphinx documentation in `docs/`
3. Consult IBM Rhapsody documentation for COM API details
