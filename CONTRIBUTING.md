# Contributing to MICS GIS Plugin

Thank you for your interest in contributing to the MICS GIS Plugin! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

This project is part of UNICEF's efforts to improve data quality for child welfare monitoring. We expect all contributors to:

- Be respectful and inclusive
- Focus on what's best for the MICS community
- Show empathy towards other contributors
- Provide constructive feedback

---

## How Can I Contribute?

### Ways to Contribute

- 🐛 **Report Bugs** - Help us identify issues
- 💡 **Suggest Features** - Propose new functionality
- 📖 **Improve Documentation** - Enhance guides and examples
- 🔧 **Fix Bugs** - Submit patches for known issues
- ✨ **Add Features** - Implement new capabilities
- 🧪 **Write Tests** - Improve test coverage
- 🌍 **Translate** - Help localize the plugin

### Good First Issues

If you're new to the project, look for issues tagged with:
- `good first issue` - Suitable for newcomers
- `documentation` - Documentation improvements
- `bug` - Bug fixes

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/mics-geocoding.git
cd mics-geocoding
```

### 2. Install Development Environment

**Requirements:**
- QGIS 3.0 or higher
- Python 3.6+ (comes with QGIS)
- Qt Designer (optional, for UI work)

**Windows:**
```batch
# Install to your QGIS plugins directory
WIN_copy.bat
```

**Linux/macOS:**
```bash
# Create symbolic link to QGIS plugins directory
ln -s $(pwd)/plugin ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/micsgeocodeplugin
```

### 3. Enable Plugin in QGIS

1. Open QGIS
2. Go to `Plugins` → `Manage and Install Plugins`
3. Find "MICS GIS PLUGIN" in the `Installed` tab
4. Check the box to activate it

### 4. Verify Installation

- The MICS GIS toolbar should appear
- Click the icon to open the plugin
- Check the QGIS log panel for any errors

---

## Coding Guidelines

### Python Style

We follow **PEP 8** with some exceptions:

```python
# Good
class CentroidsLoader:
    """Handle the loading of centroids."""
    
    def loadCentroids(self) -> Errors.ErrorCode:
        """Facade method that handles all centroid loading."""
        Logger.logInfo("[CentroidsLoader] Starting process")
        # Implementation...
```

**Key Points:**
- Use descriptive variable names
- Add docstrings to all classes and public methods
- Use type hints where practical
- Keep methods focused and single-purpose
- Comment complex algorithms

### Code Organization

- **UI Code**: `mgp_main_window*.py` files
- **Business Logic**: `micsgeocode/` package
- **Utilities**: `micsgeocode/Utils.py`, `micsgeocode/Logger.py`
- **Configuration**: `mgp_config_reader.py`, `mgp_config_writer.py`

### Logging

Use the Logger class for all logging:

```python
from .Logger import Logger

Logger.logInfo("[YourClass] Informational message")
Logger.logWarning("[YourClass] Warning message")
Logger.logError("[YourClass] Error message")
```

### Error Handling

Use the Errors module for error codes:

```python
from . import Errors

def yourMethod() -> Errors.ErrorCode:
    if something_wrong:
        return Errors.ErrorCode.ERROR_MISSING_INPUT
    return Errors.ErrorCode.SUCCESS
```

---

## Submitting Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-covariate-type` - New features
- `fix/csv-encoding-issue` - Bug fixes
- `docs/improve-user-guide` - Documentation
- `refactor/simplify-loader` - Code refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
Add support for NetCDF covariate files

- Implement NetCDF reader in CovariatesProcesser
- Add file format detection
- Update user guide with NetCDF examples
- Add tests for NetCDF processing

Fixes #123
```

**Format:**
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrapped at 72 characters)
- Reference related issues

### Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Follow coding guidelines
   - Test your changes thoroughly

3. **Update Documentation**
   - Update USER_GUIDE.md if user-facing
   - Update README.md if architecture changes
   - Add/update docstrings

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill out the PR template
   - Link related issues
   - Request review from maintainers

### Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All new code has docstrings
- [ ] Documentation is updated (if needed)
- [ ] Manual testing completed in QGIS
- [ ] No new errors in QGIS log panel
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains what and why

---

## Reporting Bugs

### Before Reporting

1. **Check existing issues** - Your bug may already be reported
2. **Try latest version** - It may already be fixed
3. **Check the User Guide** - It might be expected behavior

### Bug Report Template

When reporting bugs, include:

**Description:**
Clear description of the issue

**Steps to Reproduce:**
1. Open plugin
2. Click on...
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- QGIS Version: 3.16
- Plugin Version: 1.3.0
- Operating System: Windows 10
- Python Version: 3.9

**Log Messages:**
```
Paste relevant messages from QGIS log panel
```

**Sample Data:**
Attach sample data if possible (anonymized)

---

## Suggesting Features

### Feature Request Template

**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Why is this needed? What problem does it solve?

**Proposed Solution:**
How might this work?

**Alternatives Considered:**
What other approaches did you consider?

**Additional Context:**
Screenshots, examples, references, etc.

---

## Development Tips

### Testing Changes

**Manual Testing Workflow:**
1. Make code changes
2. Run `WIN_build.bat` (if UI/resources changed)
3. Reload plugin in QGIS (`Plugins` → `Reload Plugin`)
4. Test functionality
5. Check log panel for errors

### UI Changes

If modifying the UI:

1. **Edit in Qt Designer**
   - Open `mgp_mainwindow.ui` in Qt Designer
   - Make changes
   - Save file

2. **Rebuild UI File**
   ```batch
   WIN_build.bat
   ```
   This converts `.ui` to `.py` and `.qrc` to `_rc.py`

3. **Test in QGIS**
   - Reload plugin
   - Verify UI changes

### Debugging

**Enable Verbose Logging:**
```python
Logger.logInfo("[Debug] Variable value: " + str(variable))
```

**Use QGIS Python Console:**
```python
# Access plugin instance
plugin = qgis.utils.plugins['micsgeocodeplugin']
# Inspect variables, call methods, etc.
```

---

## Questions?

If you have questions about contributing:

- **Email**: ngashi@unicef.org
- **GitHub Issues**: For technical questions
- **Documentation**: Check USER_GUIDE.md and README.md

---

## Recognition

Contributors will be:
- Listed in release notes
- Acknowledged in the repository
- Part of improving child welfare data worldwide

Thank you for contributing to the MICS GIS Plugin! 🌍

---

## Project Authors

**Original Authors**: Jan Burdziej (UNICEF), Nazim Gashi (UNICEF), Etienne Delclaux (CartONG)

**Contributors**: See release notes and git history for full list of contributors.
