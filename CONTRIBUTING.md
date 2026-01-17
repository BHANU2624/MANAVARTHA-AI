# Contributing to MANAVARTHA-AI

Thank you for your interest in contributing to MANAVARTHA-AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or identity.

### Expected Behavior

- Be respectful and considerate
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing others' private information
- Other conduct that could be considered unprofessional

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **For Backend Development:**
   - Python 3.8 or higher
   - pip package manager
   - Virtual environment tools
   - Git

2. **For Frontend Development:**
   - Flutter SDK 3.10.1 or higher
   - Dart SDK
   - Git

3. **API Keys:**
   - Cohere API key (for development/testing)
   - Optional: Gemini API key

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MANAVARTHA-AI.git
   cd MANAVARTHA-AI
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/BHANU2624/MANAVARTHA-AI.git
   ```

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### Frontend Setup

```bash
cd telugu_news_app
flutter pub get
```

### Keep Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python/Flutter version, etc.
6. **Screenshots**: If applicable
7. **Logs**: Relevant error messages or logs

**Template:**
```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Windows 11, Ubuntu 22.04]
 - Python Version: [e.g., 3.10]
 - Flutter Version: [e.g., 3.16.0]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

1. **Use Case**: Why this enhancement would be useful
2. **Proposed Solution**: How you envision the enhancement working
3. **Alternatives**: Other solutions you've considered
4. **Additional Context**: Any other relevant information

### Submitting Changes

1. **Create a Branch**: Create a feature branch for your changes
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**: Implement your changes following our coding standards

3. **Test**: Ensure all tests pass and add new tests if needed

4. **Commit**: Use clear and meaningful commit messages
   ```bash
   git commit -m "Add feature: brief description"
   ```

5. **Push**: Push your changes to your fork
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Pull Request**: Open a pull request against the main repository

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's coding standards
- [ ] All tests pass
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up-to-date with main

### PR Description Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to not work as expected)
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe the tests you ran and their results.

## Screenshots (if applicable)
Add screenshots to demonstrate the changes.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
```

### Review Process

1. At least one maintainer will review your PR
2. Address any requested changes
3. Once approved, a maintainer will merge your PR

## Coding Standards

### Python (Backend)

#### Style Guide
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names

#### Code Organization
```python
# 1. Standard library imports
import os
import sys

# 2. Third-party imports
import numpy as np
import pandas as pd

# 3. Local imports
from .models import User
from .utils import helper_function
```

#### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this error is raised
    """
    pass
```

#### Type Hints
```python
from typing import List, Dict, Optional

def process_data(data: List[str], config: Optional[Dict] = None) -> Dict[str, int]:
    pass
```

### Dart/Flutter (Frontend)

#### Style Guide
- Follow [Effective Dart](https://dart.dev/guides/language/effective-dart)
- Use 2 spaces for indentation
- Use meaningful variable and widget names
- Organize imports: Dart SDK → Flutter → Third-party → Local

#### Widget Structure
```dart
class MyWidget extends StatelessWidget {
  // 1. Constructor
  const MyWidget({Key? key, required this.title}) : super(key: key);
  
  // 2. Fields
  final String title;
  
  // 3. Build method
  @override
  Widget build(BuildContext context) {
    return Container();
  }
  
  // 4. Helper methods
  void _helperMethod() {}
}
```

#### Comments
```dart
/// Brief description of the class/function.
///
/// More detailed explanation if needed.
///
/// Example:
/// ```dart
/// final widget = MyWidget(title: 'Hello');
/// ```
class MyWidget extends StatelessWidget {
  // ...
}
```

## Testing Guidelines

### Backend Tests

```python
import pytest

def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test"
    expected = "test_result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected
```

Run tests:
```bash
cd backend
pytest
```

### Frontend Tests

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Widget test description', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(MyWidget());
    
    // Verify
    expect(find.text('Hello'), findsOneWidget);
  });
}
```

Run tests:
```bash
cd telugu_news_app
flutter test
```

## Documentation

### When to Update Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Adding new dependencies
- Modifying configuration
- Fixing bugs that affect usage

### Documentation Files to Update

- `README.md` - Main project documentation
- `backend/README.md` - Backend-specific documentation
- `telugu_news_app/README.md` - Frontend-specific documentation
- Code comments and docstrings
- API documentation (if applicable)

### Documentation Style

- Use clear, concise language
- Include code examples
- Keep it up-to-date
- Use proper markdown formatting
- Add screenshots for UI changes

## Questions?

If you have questions:

1. Check existing documentation
2. Search existing issues
3. Open a new issue with the `question` label
4. Reach out to maintainers

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Project acknowledgments
- Release notes (for significant contributions)

Thank you for contributing to MANAVARTHA-AI! 🎉
