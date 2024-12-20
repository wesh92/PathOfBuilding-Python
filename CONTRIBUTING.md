# Contributing to the Project

<!--toc:start-->
- [Contributing to the project](#contributing-to-the-project)
  - [Getting Started](#getting-started)
  - [Development Tools](#development-tools)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
  - [GPG Commit Signing](#gpg-commit-signing)
    - [Setting up GPG commit signing:](#setting-up-gpg-commit-signing)
  - [Making Changes](#making-changes)
  - [Submitting a Pull Request](#submitting-a-pull-request)
  - [Code Style and Guidelines](#code-style-and-guidelines)
  - [Reporting Issues](#reporting-issues)
<!--toc:end-->

Thank you for your interest in contributing to Path of Building - Python Fork/Port! We welcome contributions from the community to help improve and expand this project. This document outlines the process for contributing and provides some guidelines to follow.

## Getting Started

Before you begin, please make sure you have:

- Git installed on your local machine
- Python 3.12.7 or higher installed
- GPG installed for commit signing

## Development Tools

We use several tools to maintain code quality and consistency:

- **UV**: A dependency management and packaging tool that simplifies Python project management.
- **Ruff**: A fast Python linter that helps catch errors and enforce coding standards.

These tools help us maintain a high standard of code quality, improve collaboration, and reduce the time spent on code formatting and style discussions.

## Setting Up the Development Environment

1. Fork or clone the repository on GitHub.
   ```
   git clone git@github.com:wesh92/PathOfBuilding-Python.git
   cd PathOfBuilding-Python
   ```
2. Install `UV`.
   ```
   https://docs.astral.sh/uv/getting-started/installation/
   ```
3. Start the venv/sync
   ```
   uv venv
   # or uv sync
   # if you already have a local venv
   ```

## GPG Commit Signing

We strongly recommend using GPG to sign your commits. This helps verify the authenticity of your contributions and increases the overall security of the project.

### Setting up GPG commit signing:

1. If you haven't already, [generate a new GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key).

2. Add your GPG key to your GitHub account by following [these instructions](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-new-gpg-key-to-your-github-account).

3. Configure Git to use your GPG key:
   ```
   git config --global user.signingkey YOUR-GPG-KEY-ID
   git config --global commit.gpgsign true
   ```

4. To sign commits in the CLI, simply use the `-S` flag with your commit command:
   ```
   git commit -S -m "Your commit message"
   ```

   If you've set `commit.gpgsign` to true globally, you can omit the `-S` flag:
   ```
   git commit -m "Your commit message"
   ```

5. To sign tags, use:
   ```
   git tag -s tagname -m "Tag message"
   ```

By using GPG signing, you help ensure the integrity and authenticity of your contributions to the project.

## Making Changes

> [!IMPORTANT]
> Use the branch names to indicate the kind of update you are working on. 
>
> Examples: for a bugfix: bugfix/module-group-affected/ISSUE-#-bugfix
> for a new feature: feature/module-group-affected-or-added/ISSUE-#-feature-stuff

1. **Make sure you have created an issue (if there wasn't one already) first. This helps with resolution tracking and proper contribution!**

2. Create a new branch for your feature or bugfix (you may not commit to the main branch directly):
   ```
   git checkout -b feature/module-group-affected-or-added/ISSUE-#-feature-stuff
   ```
3. Make your changes, ensuring you follow the code style guidelines.
4. Run Ruff to check for linting errors:
   ```
   uv run ruff check .
   uv run ruff format .
   ```
5. Commit your changes with a clear and descriptive commit message, signing your commit:
   ```
   git commit -S -m "Add feature: description of your changes"
   ```
6. Push your changes to your fork:
   ```
   git push
   ```

## Submitting a Pull Request

1. Go to the original repository on GitHub.
2. Click on "New Pull Request" and select your fork (if you made a fork) and/or branch.
3. Fill out the pull request with a clear title and description of your changes. See the template for details.
4. Ensure all checks (linting, formatting, tests) pass before requesting a review.
5. Submit the pull request for review.

## Code Style and Guidelines

> [!IMPORTANT]
> Please see the CODE_STYLE.md for more detailed information. Reading this section should not supplant anything in that document!

- Use Ruff for code formatting to ensure consistency.
- Use Ruff for linting to catch potential errors and style issues.
- Use meaningful variable and function names (avoid single letter names, for instance).
- Write clear comments and docstrings for functions and classes.
  - Please use google-style docstrings.
- Keep functions small and focused on a single task.
- Use type hints.
- Write unit tests for new functionality where possible.

## Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the GitHub issue tracker.
2. If not, create a new issue with a clear title and description.
3. Include steps to reproduce the issue if it's a bug.
4. Add relevant labels to the issue.

Thank you for contributing!