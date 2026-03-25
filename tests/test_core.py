"""Tests for Zeus core functionality."""

import tempfile
from pathlib import Path

from zeus.core import AppGenerator, ParsedDescription
from zeus.templates import TEMPLATES, TemplateEngine


class TestParseDescription:
    """Tests for description parsing."""

    def test_parse_api_description(self) -> None:
        gen = AppGenerator()
        result = gen.parse_description("A REST API for managing users")
        assert result.project_type == "api"
        assert result.project_name

    def test_parse_webapp_description(self) -> None:
        gen = AppGenerator()
        result = gen.parse_description("A web dashboard for analytics")
        assert result.project_type == "webapp"

    def test_parse_cli_description(self) -> None:
        gen = AppGenerator()
        result = gen.parse_description("A CLI tool for file management")
        assert result.project_type == "cli"

    def test_parse_features(self) -> None:
        gen = AppGenerator()
        result = gen.parse_description("An API with authentication and rate limiting")
        assert len(result.features) >= 1

    def test_parse_default_type(self) -> None:
        gen = AppGenerator()
        result = gen.parse_description("Something cool")
        assert result.project_type == "webapp"


class TestSelectTemplate:
    """Tests for template selection."""

    def test_select_api_template(self) -> None:
        gen = AppGenerator()
        template = gen.select_template("api")
        assert template.project_type == "api"
        assert len(template.files) > 0

    def test_select_webapp_template(self) -> None:
        gen = AppGenerator()
        template = gen.select_template("webapp")
        assert template.project_type == "webapp"

    def test_select_unknown_falls_back(self) -> None:
        gen = AppGenerator()
        template = gen.select_template("unknown")
        assert template.project_type == "webapp"


class TestTemplateEngine:
    """Tests for the template rendering engine."""

    def test_render_simple(self) -> None:
        engine = TemplateEngine()
        result = engine.render("Hello {{ name }}", {"name": "World"})
        assert result == "Hello World"

    def test_list_templates(self) -> None:
        engine = TemplateEngine()
        templates = engine.list_templates()
        assert len(templates) == len(TEMPLATES)


class TestGenerateFiles:
    """Tests for file generation."""

    def test_generate_creates_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = AppGenerator(output_dir=Path(tmpdir))
            template = gen.select_template("cli")
            variables = {
                "project_name": "test-app",
                "description": "A test app",
                "features": [],
                "project_type": "cli",
            }
            output_path = Path(tmpdir) / "test-app"
            output_path.mkdir()
            files = gen.generate_files(template, variables, output_path)
            assert len(files) > 0
            assert "README.md" in files


class TestScaffoldProject:
    """Tests for the full scaffolding pipeline."""

    def test_scaffold_creates_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = AppGenerator(output_dir=Path(tmpdir))
            result = gen.scaffold_project("A REST API for managing tasks")
            assert result.output_path.exists()
            assert len(result.files_created) > 0
            assert result.project_type == "api"
