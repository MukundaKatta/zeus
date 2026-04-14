# zeus — AI App Builder. Full-stack AI app builder

AI App Builder. Full-stack AI app builder.

## Why zeus

zeus exists to make this workflow practical. Ai app builder. full-stack ai app builder. It favours a small, inspectable surface over sprawling configuration.

## Features

- CLI command `zeus`
- `ParsedDescription` — exported from `src/zeus/core.py`
- `GeneratedProject` — exported from `src/zeus/core.py`
- `AppGenerator` — exported from `src/zeus/core.py`
- Included test suite
- Dedicated documentation folder

## Tech Stack

- **Runtime:** Python
- **Frameworks:** Click
- **Tooling:** Pydantic, Rich

## How It Works

The codebase is organised into `docs/`, `src/`, `tests/`. The primary entry points are `src/zeus/core.py`, `src/zeus/cli.py`, `src/zeus/__init__.py`. `src/zeus/core.py` exposes `ParsedDescription`, `GeneratedProject`, `AppGenerator` — the core types that drive the behaviour. `src/zeus/cli.py` exposes functions like `main`, `generate`, `list_templates`.

## Getting Started

```bash
pip install -e .
zeus --help
```

## Usage

```bash
zeus --help
```

## Project Structure

```
zeus/
├── .env.example
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── README.md
├── docs/
├── pyproject.toml
├── src/
├── tests/
```