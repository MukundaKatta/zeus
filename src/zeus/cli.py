"""Zeus CLI — generate apps from natural language."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from zeus.core import AppGenerator
from zeus.templates import TEMPLATES, TemplateEngine
from zeus.config import load_config
from zeus.utils import format_success, format_error

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="zeus")
def main() -> None:
    """Zeus — Build full-stack apps from natural language descriptions."""
    pass


@main.command()
@click.argument("description")
@click.option("--output", "-o", type=click.Path(), default=None, help="Output directory")
@click.option("--type", "project_type", type=click.Choice(["api", "webapp", "cli"]), default=None)
def generate(description: str, output: str | None, project_type: str | None) -> None:
    """Generate an application from a natural language description."""
    config = load_config()
    output_dir = Path(output) if output else config.output_dir

    generator = AppGenerator(output_dir=output_dir)

    console.print(f"\n[bold blue]⚡ Zeus[/bold blue] generating project...\n")

    parsed = generator.parse_description(description)
    if project_type:
        parsed.project_type = project_type

    console.print(f"  Project: [bold]{parsed.project_name}[/bold]")
    console.print(f"  Type:    [cyan]{parsed.project_type}[/cyan]")
    if parsed.features:
        console.print(f"  Features: {', '.join(parsed.features)}")

    result = generator.scaffold_project(description)

    console.print()
    format_success(f"Created {len(result.files_created)} files in {result.output_path}")
    for f in result.files_created:
        console.print(f"    [dim]→ {f}[/dim]")
    console.print()


@main.command("list-templates")
def list_templates() -> None:
    """List all available project templates."""
    engine = TemplateEngine()
    templates = engine.list_templates()

    table = Table(title="Available Templates")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Files", justify="right")

    for t in templates:
        table.add_row(t["type"], t["name"], t["description"], t["files"])

    console.print(table)


@main.command()
@click.argument("name")
@click.option("--type", "project_type", type=click.Choice(["api", "webapp", "cli"]), default="webapp")
def init(name: str, project_type: str) -> None:
    """Initialize a new project directory with a template."""
    config = load_config()
    generator = AppGenerator(output_dir=config.output_dir)

    template = generator.select_template(project_type)
    output_path = config.output_dir / name
    output_path.mkdir(parents=True, exist_ok=True)

    variables = {
        "project_name": name,
        "description": f"A new {project_type} project",
        "features": [],
        "project_type": project_type,
    }

    files = generator.generate_files(template, variables, output_path)
    format_success(f"Initialized {name} ({project_type}) with {len(files)} files at {output_path}")


if __name__ == "__main__":
    main()
