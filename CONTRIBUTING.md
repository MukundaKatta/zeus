# Contributing to Zeus

We welcome contributions! Here's how to get started.

## Setup

```bash
git clone https://github.com/MukundaKatta/zeus.git
cd zeus
pip install -e ".[dev]"
```

## Development

```bash
make lint      # Run linter
make test      # Run tests
make format    # Format code
```

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make your changes with tests
4. Run `make lint && make test`
5. Submit a pull request

## Code Style

- Use type hints on all functions
- Add docstrings to classes and public methods
- Follow PEP 8 conventions
- Keep functions focused and small
