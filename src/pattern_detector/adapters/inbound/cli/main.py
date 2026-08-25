import os
import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markup import escape

from ....domain.pattern import PATTERN_CATALOG
from ....domain.detection import DetectionReport
from ....application.scan_service import ScanService
from ..parsers.ruby_parser import RegexRubyParser
from ..detectors.ruby_detector import RubyPatternDetector

app = typer.Typer(help="💎 DPX-Ruby: Architectural Pattern & Static Analysis Engine for Ruby 3.x & Rails")
console = Console()


@app.command()
def version():
    """Print DPX-Ruby version and engine info."""
    console.print(
        Panel(
            "[bold red]💎 DPX-Ruby v0.1.0[/bold red]\n"
            "[white]Hexagonal DDD Static Analysis Engine for Ruby 3.x & Ruby on Rails[/white]\n"
            "[dim]https://github.com/bivex/DPX-Ruby[/dim]",
            title="Engine Info",
            border_style="red",
        )
    )


@app.command()
def catalog():
    """Display the 42 supported architectural patterns and hazard catalog."""
    table = Table(
        title="📚 DPX-Ruby Supported Pattern Catalog (42 Rules)",
        header_style="bold red",
        border_style="dim",
    )
    table.add_column("Pattern Type", style="bold white")
    table.add_column("Category", style="green")
    table.add_column("Default Weight", justify="center", style="cyan")
    table.add_column("Description", style="dim")

    for p_type, meta in PATTERN_CATALOG.items():
        weight_str = f"{int(meta.default_weight * 100)}%"
        table.add_row(meta.pattern_type.value, meta.category.value, weight_str, meta.description)

    console.print(table)


@app.command()
def scan(
    paths: List[str] = typer.Argument(..., help="Path(s) to Ruby file(s) (.rb, .rake) or directory"),
    html: Optional[str] = typer.Option(None, "--html", "-H", help="Path to export interactive HTML HUD report"),
    json_path: Optional[str] = typer.Option(None, "--json", "-J", help="Path to export findings JSON report"),
    markdown: Optional[str] = typer.Option(None, "--markdown", "-M", help="Path to export findings Markdown report"),
    sarif: Optional[str] = typer.Option(None, "--sarif", "-S", help="Path to export SARIF v2.1.0 report"),
):
    """Scan Ruby codebases for architectural patterns, metaprogramming, and security hazards."""
    parser = RegexRubyParser()
    detector = RubyPatternDetector()
    service = ScanService(parser=parser, detector=detector)

    with console.status("[bold red]Scanning Ruby codebase for architectural patterns...[/bold red]"):
        report = service.scan_paths(
            paths=paths,
            html_out=html,
            json_out=json_path,
            md_out=markdown,
            sarif_out=sarif,
        )

    # Render summary table
    table = Table(
        title=f"💎 DPX-Ruby Findings Summary ({report.total_detections} detected in {report.execution_time_seconds:.4f}s)",
        header_style="bold red",
        border_style="red",
    )
    table.add_column("#", justify="center", style="dim")
    table.add_column("Category", style="green")
    table.add_column("Pattern Type", style="bold white")
    table.add_column("Target Symbol", style="cyan")
    table.add_column("Confidence", justify="center", style="yellow")
    table.add_column("Location", style="dim")

    for idx, d in enumerate(report.detections, start=1):
        loc_str = f"{os.path.basename(d.location.file_path)}:{d.location.line_number}"
        conf_str = f"{d.confidence.percentage}%\n[{d.confidence.level.value}]"
        table.add_row(
            str(idx),
            escape(d.category.value),
            escape(d.pattern_type.value),
            escape(d.target_name),
            conf_str,
            escape(loc_str),
        )

    console.print(table)

    if html:
        console.print(f"[bold green]✔[/bold green] Interactive HTML HUD exported to: [red]{html}[/red]")
    if json_path:
        console.print(f"[bold green]✔[/bold green] JSON findings exported to: [red]{json_path}[/red]")
    if markdown:
        console.print(f"[bold green]✔[/bold green] Markdown report exported to: [red]{markdown}[/red]")
    if sarif:
        console.print(f"[bold green]✔[/bold green] SARIF file exported to: [red]{sarif}[/red]")


if __name__ == "__main__":
    app()
