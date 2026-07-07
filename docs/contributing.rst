Contributing
=============

Thank you for your interest in contributing to rhapsody-cli! This guide explains how to contribute effectively.

Getting Started
---------------

1. **Fork the Repository**

   Fork the repository on GitHub: https://github.com/melodypapa/rhapsody-cli

2. **Clone Your Fork**

   .. code-block:: bash

      git clone https://github.com/YOUR_USERNAME/rhapsody-cli.git
      cd rhapsody-cli

3. **Create a Feature Branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name

4. **Install Development Dependencies**

   .. code-block:: bash

      pip install -e ".[dev,cli]"

Development Workflow
--------------------

Code Style
~~~~~~~~~~

* Follow PEP 8 style guidelines
* Use 4 spaces for indentation
* Maximum line length: 100 characters
* Type annotations required for all functions

Formatting and Linting
~~~~~~~~~~~~~~~~~~~~~~

Run these tools before committing:

.. code-block:: bash

   # Linting
   ruff check src/ tests/

   # Formatting
   black src/ tests/

   # Type checking
   mypy src/ tests/

   # All checks
   ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/

Testing
~~~~~~~

All changes must have tests:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=src/rhapsody_cli tests/

   # Run specific test
   pytest tests/test_application.py

Test-Driven Development (TDD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rhapsody-cli follows TDD principles:

1. Write tests first
2. Run tests (they should fail)
3. Write minimal code to pass tests
4. Refactor while tests pass

.. code-block:: bash

   # Add test file: tests/test_new_feature.py
   # Run test
   pytest tests/test_new_feature.py  # Should fail

   # Write implementation in src/
   # Run test again
   pytest tests/test_new_feature.py  # Should pass

Documentation
~~~~~~~~~~~~~

Update documentation for changes:

* Add docstrings to all functions and classes
* Update relevant .rst files in docs/
* Run Sphinx to verify documentation builds

.. code-block:: bash

   cd docs
   make html

Git Workflow
------------

1. **Make Your Changes**

   .. code-block:: bash

      git add src/rhapsody_cli/your_changes.py tests/test_your_feature.py

2. **Run Quality Checks**

   .. code-block:: bash

      ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest

3. **Commit Your Changes**

   .. code-block:: bash

      git commit -m "feat: describe your feature

      Longer description of changes if needed.
      - Bullet point 1
      - Bullet point 2"

   **Commit message format:**
   * `feat:` - New feature
   * `fix:` - Bug fix
   * `docs:` - Documentation
   * `refactor:` - Code reorganization
   * `test:` - Test additions
   * `chore:` - Build/dependency updates

4. **Push to Your Fork**

   .. code-block:: bash

      git push -u origin feature/your-feature-name

5. **Create a Pull Request**

   Go to https://github.com/melodypapa/rhapsody-cli/compare and create a PR from your fork.

Pull Request Guidelines
-----------------------

* **Title**: Use the commit message format (e.g., "feat: add new element type")
* **Description**: Explain what the PR does and why
* **Tests**: Include tests for new features
* **Documentation**: Update docs if relevant
* **No breaking changes**: Maintain backward compatibility

Example PR Description
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ## Description
   Adds support for diagrams in rhapsody-cli.

   ## Changes
   - Add RPDiagram element wrapper
   - Add diagram methods to RPProject
   - Add diagram query to CLI

   ## Testing
   - Added 12 new tests in tests/models/elements/test_diagram.py
   - All 173 tests pass

   ## Related Issues
   Closes #42

Code Review Process
-------------------

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Manual Review**: Project maintainers review your code
3. **Feedback**: Respond to feedback and make requested changes
4. **Approval**: Once approved, your PR will be merged

Reporting Issues
----------------

Found a bug? Open an issue with:

1. **Title**: Clear, concise description
2. **Steps to Reproduce**: How to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, Rhapsody version, OS
6. **Screenshots**: If applicable

Example Issue
~~~~~~~~~~~~~

.. code-block:: text

   Title: RPClass.createAttribute() fails with None type

   Steps to Reproduce:
   1. Create a class
   2. Call createAttribute("name", None)

   Expected: Should handle None gracefully
   Actual: Raises AttributeError

   Environment:
   - Python 3.9
   - rhapsody-cli 0.1.0
   - Windows 10
   - Rhapsody 8.3

Getting Help
~~~~~~~~~~~~

* Check existing issues and discussions
* Read the documentation
* Ask in GitHub discussions

Code of Conduct
---------------

Be respectful and constructive in all interactions. We're all here to make rhapsody-cli better!

License
-------

By contributing to rhapsody-cli, you agree that your contributions will be licensed under the MIT License.

Architecture Guidelines
-----------------------

Before contributing, familiarize yourself with the architecture:

* **Models Layer** (`src/rhapsody_cli/models/`): Element wrappers
* **Application Layer** (`src/rhapsody_cli/application.py`): Connection management
* **CLI Layer** (`src/rhapsody_cli/cli/`): Command-line interface
* **Test Layer** (`tests/`): Unit tests with fakes

See the main documentation for architecture details.

Resources
---------

* **Main Repository**: https://github.com/melodypapa/rhapsody-cli
* **Issue Tracker**: https://github.com/melodypapa/rhapsody-cli/issues
* **Documentation**: https://rhapsody-cli.readthedocs.io/
* **Python Packaging**: https://packaging.python.org/

Thank you for contributing!
