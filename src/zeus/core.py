"""Core logic for Zeus — the AI app generator."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from zeus.templates import TEMPLATES, ProjectTemplate, TemplateEngine
from zeus.utils import ensure_dir, slugify


# Keywords that map to project types
TYPE_KEYWORDS: dict[str, list[str]] = {
    "api": [
        "api", "rest", "endpoint", "backend", "server", "microservice",
        "graphql", "crud", "database",
    ],
    "webapp": [
        "web", "website", "frontend", "dashboard", "portal", "page",
        "ui", "interface", "app", "application", "full-stack", "fullstack",
    ],
    "cli": [
        "cli", "command", "terminal", "console", "tool", "script", "utility",
    ],
}


@dataclass
class ParsedDescription:
    """Parsed result from a natural language project description."""

    raw: str
    project_name: str
    project_type: str
    features: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)


@dataclass
class GeneratedProject:
    """Result of a project generation run."""

    name: str
    project_type: str
    output_path: Path
    files_created: list[str] = field(default_factory=list)
    template_used: str = ""


class AppGenerator:
    """Generate full-stack applications from natural language descriptions.

    The generator parses a description, selects an appropriate template,
    and scaffolds a complete project directory with working code.
    """

    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or Path("./generated")
        self.engine = TemplateEngine()

    def parse_description(self, description: str) -> ParsedDescription:
        """Parse a natural language description into structured project info.

        Extracts the project name, type, features, and entities from
        the description using keyword matching.
        """
        lower = description.lower()
        words = re.findall(r"\b\w+\b", lower)

        # Detect project type by keyword frequency
        scores: dict[str, int] = {pt: 0 for pt in TYPE_KEYWORDS}
        for word in words:
            for project_type, keywords in TYPE_KEYWORDS.items():
                if word in keywords:
                    scores[project_type] += 1

        best_type = max(scores, key=lambda k: scores[k])
        if scores[best_type] == 0:
            best_type = "webapp"  # default

        # Extract a project name from the first noun-like phrase
        project_name = self._extract_project_name(description)

        # Extract features — phrases after "with" or listed items
        features = self._extract_features(description)

        # Extract entities — capitalized words or quoted strings
        entities = re.findall(r'"([^"]+)"', description)
        entities += [w for w in description.split() if w[0:1].isupper() and len(w) > 2]

        return ParsedDescription(
            raw=description,
            project_name=project_name,
            project_type=best_type,
            features=features,
            entities=list(set(entities)),
        )

    def select_template(self, project_type: str) -> ProjectTemplate:
        """Select the best template for the given project type.

        Falls back to the webapp template if the type is not found.
        """
        return TEMPLATES.get(project_type, TEMPLATES["webapp"])

    def generate_files(
        self,
        template: ProjectTemplate,
        variables: dict[str, Any],
        output_path: Path,
    ) -> list[str]:
        """Generate all project files from a template.

        Returns a list of file paths that were created.
        """
        rendered = self.engine.render_template(template, variables)
        created: list[str] = []

        for file_path, content in rendered:
            full_path = output_path / file_path
            ensure_dir(full_path.parent)
            full_path.write_text(content, encoding="utf-8")
            created.append(file_path)

        # Always generate a README
        readme_content = self._generate_readme(variables, template)
        readme_path = output_path / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")
        created.append("README.md")

        return created

    def scaffold_project(self, description: str) -> GeneratedProject:
        """Run the full generation pipeline from description to project.

        This is the main entry point: parse → select → generate.
        """
        parsed = self.parse_description(description)
        template = self.select_template(parsed.project_type)
        output_path = ensure_dir(self.output_dir / parsed.project_name)

        variables = {
            "project_name": parsed.project_name,
            "description": parsed.raw,
            "features": parsed.features,
            "project_type": parsed.project_type,
        }

        files = self.generate_files(template, variables, output_path)

        return GeneratedProject(
            name=parsed.project_name,
            project_type=parsed.project_type,
            output_path=output_path,
            files_created=files,
            template_used=template.name,
        )

    # ── Private helpers ───────────────────────────────────────────

    @staticmethod
    def _extract_project_name(description: str) -> str:
        """Extract a project name from the description."""
        # Try to find a quoted name first
        quoted = re.findall(r'"([^"]+)"', description)
        if quoted:
            return slugify(quoted[0])

        # Otherwise use first few meaningful words
        stop_words = {"a", "an", "the", "with", "and", "or", "for", "that", "this"}
        words = [w for w in description.split()[:6] if w.lower() not in stop_words]
        name = "-".join(words[:3]).lower()
        return slugify(name) or "my-project"

    @staticmethod
    def _extract_features(description: str) -> list[str]:
        """Extract feature descriptions from the text."""
        features: list[str] = []
        # Split on "with", "and", commas
        parts = re.split(r"\bwith\b|\band\b|,", description, flags=re.IGNORECASE)
        for part in parts[1:]:
            cleaned = part.strip().strip(".")
            if len(cleaned) > 3:
                features.append(cleaned)
        return features

    @staticmethod
    def _generate_readme(variables: dict[str, Any], template: ProjectTemplate) -> str:
        """Generate a README.md file for the project."""
        name = variables.get("project_name", "project")
        desc = variables.get("description", "")
        features = variables.get("features", [])

        lines = [
            f"# {name}\n",
            f"> {desc}\n",
            f"Generated with Zeus using the **{template.name}** template.\n",
            "## Getting Started\n",
            "```bash",
            "pip install -r requirements.txt",
        ]

        if template.project_type == "api":
            lines.append('uvicorn app.main:app --reload')
        elif template.project_type == "webapp":
            lines.append('uvicorn backend.main:app --reload')
        else:
            lines.append("python -m src.main")

        lines.append("```\n")

        if features:
            lines.append("## Features\n")
            for feat in features:
                lines.append(f"- {feat}")
            lines.append("")

        return "\n".join(lines) + "\n"
