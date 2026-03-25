"""Utility functions for Zeus."""

import re
from pathlib import Path

from rich.console import Console

console = Console()


def ensure_dir(path: Path) -> Path:
    """Create directory if it does not exist and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def slugify(text: str) -> str:
    """Convert text to a URL/filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def validate_name(name: str) -> bool:
    """Validate a project name contains only allowed characters."""
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))


def format_output(message: str, style: str = "green") -> None:
    """Print formatted output to the console."""
    console.print(f"[{style}]{message}[/{style}]")


def format_error(message: str) -> None:
    """Print an error message to the console."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def format_success(message: str) -> None:
    """Print a success message to the console."""
    console.print(f"[bold green]✓[/bold green] {message}")


def count_files(directory: Path) -> int:
    """Count files recursively in a directory."""
    if not directory.exists():
        return 0
    return sum(1 for _ in directory.rglob("*") if _.is_file())
