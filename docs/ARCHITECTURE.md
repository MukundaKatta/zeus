# Zeus Architecture

## Overview

Zeus follows a pipeline architecture for transforming natural language descriptions into working projects.

## Components

### CLI Layer (`cli.py`)
Entry point for all user interactions. Provides `generate`, `list-templates`, and `init` commands.

### Core Engine (`core.py`)
The `AppGenerator` class orchestrates the pipeline:
1. **Parse** — Extract project name, type, features from description
2. **Select** — Choose the best template for the project type
3. **Generate** — Render template files with project-specific variables

### Template System (`templates.py`)
- `ProjectTemplate` — Defines a project type with file templates and dependencies
- `TemplateEngine` — Jinja2-based renderer for template strings
- Built-in templates: API, WebApp, CLI

### Configuration (`config.py`)
Pydantic-based settings loaded from environment variables and `.env` files.

## Data Flow

```
User Description → Parser → Template Selector → Template Engine → File Writer → Project Directory
```
