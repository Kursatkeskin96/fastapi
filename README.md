# Project Overview

This project is built with FastAPI, a modern web framework for building APIs with Python 3.7+ based on standard Python type hints. The Makefile included in this project simplifies the process of setting up your development environment, installing dependencies, and running the application in both development and production environments.

## Prerequisites

Before using the Makefile, ensure that you have the following installed on your system:

- Python 3.10+
- `pip3` (Python package installer)
- `make` utility

## Usage

Run `make venv` and run `source ./venv/bin/activate` in terminal, then follow this documentation

The Makefile contains several commands to help streamline the workflow. Below is a description of each target and how to use them.

### 1. `make run-dev`

**Description:**  
This target sets up the development environment and runs the application in development mode.

**Steps executed:**

- Creates a virtual environment (`venv`) if it doesn't already exist.
- Installs all required dependencies from `requirements.txt`.
- Starts the FastAPI application in development mode using the `fastapi dev` command.

**Command:**

```sh
make run-dev
