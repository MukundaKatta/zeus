"""Template definitions and rendering engine for Zeus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jinja2 import Environment, BaseLoader


@dataclass
class FileTemplate:
    """A single file to generate within a project."""

    path: str
    content: str
    executable: bool = False


@dataclass
class ProjectTemplate:
    """A project template with metadata and file definitions."""

    name: str
    description: str
    project_type: str
    files: list[FileTemplate] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


TEMPLATES: dict[str, ProjectTemplate] = {
    "api": ProjectTemplate(
        name="FastAPI REST API",
        description="Production-ready REST API with FastAPI, SQLAlchemy, and Pydantic",
        project_type="api",
        files=[
            FileTemplate("app/__init__.py", ""),
            FileTemplate(
                "app/main.py",
                '''"""{{ project_name }} — FastAPI application."""
from fastapi import FastAPI

app = FastAPI(title="{{ project_name }}", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Welcome to {{ project_name }}"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
''',
            ),
            FileTemplate(
                "app/models.py",
                '''"""Database models for {{ project_name }}."""
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str = ""


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    model_config = {"from_attributes": True}
''',
            ),
            FileTemplate(
                "app/config.py",
                '''"""Configuration for {{ project_name }}."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "{{ project_name }}"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"

    model_config = {"env_file": ".env"}


settings = Settings()
''',
            ),
            FileTemplate(
                "requirements.txt",
                "fastapi>=0.104\nuvicorn>=0.24\npydantic>=2.0\npydantic-settings>=2.0\n",
            ),
            FileTemplate(
                "Dockerfile",
                """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
            ),
        ],
        dependencies=["fastapi", "uvicorn", "pydantic", "pydantic-settings"],
    ),
    "webapp": ProjectTemplate(
        name="Full-Stack Web Application",
        description="Web application with FastAPI backend and HTML/JS frontend",
        project_type="webapp",
        files=[
            FileTemplate("backend/__init__.py", ""),
            FileTemplate(
                "backend/main.py",
                '''"""{{ project_name }} — Web application backend."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="{{ project_name }}")
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def index():
    return FileResponse("frontend/index.html")


@app.get("/api/health")
async def health():
    return {"status": "healthy"}
''',
            ),
            FileTemplate(
                "frontend/index.html",
                """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
        h1 { color: #2563eb; }
    </style>
</head>
<body>
    <h1>{{ project_name }}</h1>
    <p>{{ description }}</p>
    <div id="app"></div>
    <script src="/static/app.js"></script>
</body>
</html>
""",
            ),
            FileTemplate(
                "frontend/app.js",
                """// {{ project_name }} frontend
document.addEventListener('DOMContentLoaded', async () => {
    const res = await fetch('/api/health');
    const data = await res.json();
    document.getElementById('app').textContent = `API Status: ${data.status}`;
});
""",
            ),
            FileTemplate(
                "requirements.txt",
                "fastapi>=0.104\nuvicorn>=0.24\npython-multipart>=0.0.6\n",
            ),
        ],
        dependencies=["fastapi", "uvicorn", "python-multipart"],
    ),
    "cli": ProjectTemplate(
        name="CLI Application",
        description="Command-line application with Click and Rich",
        project_type="cli",
        files=[
            FileTemplate("src/__init__.py", ""),
            FileTemplate(
                "src/main.py",
                '''"""{{ project_name }} — CLI application."""
import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """{{ description }}"""
    pass


@cli.command()
@click.argument("name", default="World")
def hello(name: str):
    """Greet someone."""
    console.print(f"[bold green]Hello, {name}![/bold green]")


@cli.command()
def status():
    """Show application status."""
    console.print("[bold]{{ project_name }}[/bold] v0.1.0")
    console.print("[green]Status: Running[/green]")


if __name__ == "__main__":
    cli()
''',
            ),
            FileTemplate(
                "requirements.txt",
                "click>=8.1\nrich>=13.0\n",
            ),
        ],
        dependencies=["click", "rich"],
    ),
}


class TemplateEngine:
    """Render project templates using Jinja2."""

    def __init__(self) -> None:
        self._env = Environment(loader=BaseLoader(), keep_trailing_newline=True)

    def render(self, content: str, variables: dict[str, Any]) -> str:
        """Render a template string with the given variables."""
        template = self._env.from_string(content)
        return template.render(**variables)

    def render_template(
        self, template: ProjectTemplate, variables: dict[str, Any]
    ) -> list[tuple[str, str]]:
        """Render all files in a project template.

        Returns a list of (path, rendered_content) tuples.
        """
        rendered: list[tuple[str, str]] = []
        for file_tmpl in template.files:
            rendered_content = self.render(file_tmpl.content, variables)
            rendered.append((file_tmpl.path, rendered_content))
        return rendered

    def list_templates(self) -> list[dict[str, str]]:
        """List all available templates with metadata."""
        return [
            {
                "name": t.name,
                "type": key,
                "description": t.description,
                "files": str(len(t.files)),
            }
            for key, t in TEMPLATES.items()
        ]
