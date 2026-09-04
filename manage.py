#!/usr/bin/env python3
"""
Unified CLI for Gemini Enterprise Eval Studio

Entrypoint for CLI commands, service operations, and development workflows.
"""

from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console


# Resolve root relative to this file for cross-worktree portability
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

console = Console()

app = typer.Typer(
    name="gemini-enterprise-eval-studio",
    help="Unified management CLI for Gemini Enterprise Eval Studio",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.callback()
def main_callback() -> None:
    """Gemini Enterprise Eval Studio CLI Operations."""
    pass


@app.command("info")
def info() -> None:
    """Display project configuration and environment status."""
    console.print(
        "[bold blue]Gemini Enterprise Eval Studio[/bold blue] Environment Status"
    )
    console.print(f"Base Directory: [cyan]{BASE_DIR}[/cyan]")


if __name__ == "__main__":
    app()
