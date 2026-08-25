import os
import pytest
from typer.testing import CliRunner
from pattern_detector.adapters.inbound.cli.main import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "DPX-Ruby" in result.stdout


def test_cli_catalog():
    result = runner.invoke(app, ["catalog"], env={"COLUMNS": "300"})
    assert result.exit_code == 0
    assert "activesupport_concern" in result.stdout
    assert "sql_injection_hazard" in result.stdout


def test_cli_scan(tmp_path):
    rb_file = tmp_path / "user.rb"
    rb_file.write_text("""
    class User < ApplicationRecord
      has_many :posts
    end
    """)

    html_out = tmp_path / "hud.html"
    json_out = tmp_path / "res.json"

    result = runner.invoke(
        app,
        [
            "scan",
            str(tmp_path),
            "--html",
            str(html_out),
            "--json",
            str(json_out),
        ],
    )
    assert result.exit_code == 0
    assert html_out.exists()
    assert json_out.exists()
