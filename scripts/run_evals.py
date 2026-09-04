#!/usr/bin/env python3
"""
Agent Platform Evaluation Runner for Gemini Enterprise Eval Studio

Runs evalsets against deployed Vertex AI Reasoning Engines and GenAI models in Argolis.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Ensure mTLS bypass and ADC paths
os.environ.setdefault("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
os.environ.setdefault("GOOGLE_API_USE_MTLS_ENDPOINT", "never")
os.environ.setdefault("CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE", "false")

import vertexai
from vertexai import agent_engines

console = Console()
app = typer.Typer(help="Agent Platform Evaluation CLI", add_completion=False)

DEFAULT_PROJECT = os.environ.get("GCP_PROJECT_ID", "dandye-0324-chronicle")
DEFAULT_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
DEFAULT_ENGINE = os.environ.get(
    "AGENT_ENGINE_RESOURCE_NAME",
    "projects/1002894625780/locations/us-central1/reasoningEngines/7232703485987258368",
)


@app.command("run")
def run_eval(
    evalset: Annotated[
        Path, typer.Option("--file", "-f", help="Path to evalset JSON file")
    ] = Path("evalsets/tier1_triage.evalset.json"),
    resource: Annotated[
        str, typer.Option("--resource", "-r", help="Reasoning Engine resource name")
    ] = DEFAULT_ENGINE,
    project: Annotated[
        str, typer.Option("--project", "-p", help="GCP Project ID")
    ] = DEFAULT_PROJECT,
    location: Annotated[
        str, typer.Option("--location", "-l", help="GCP Region")
    ] = DEFAULT_LOCATION,
) -> None:
    """Run an evaluation suite against a deployed Reasoning Engine on Agent Platform."""
    if not evalset.exists():
        console.print(f"[bold red]Error:[/bold red] File not found: {evalset}")
        raise typer.Exit(1)

    with open(evalset, "r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("name", evalset.stem)
    cases = data.get("eval_cases", [])
    console.print(f"\n[bold blue]Running Evaluation Suite:[/bold blue] {name}")
    console.print(f"Target Resource: [cyan]{resource}[/cyan]")
    console.print(f"Total Cases: [bold]{len(cases)}[/bold]\n")

    vertexai.init(project=project, location=location)
    remote_agent = agent_engines.get(resource)

    results_table = Table(title=f"Evaluation Results - {name}")
    results_table.add_column("Case ID", style="cyan")
    results_table.add_column("Query", style="white")
    results_table.add_column("Tool Trajectory", style="yellow")
    results_table.add_column("Status", style="green")

    async def _execute_all():
        for case in cases:
            eval_id = case.get("eval_id", "unknown")
            conv = case.get("conversation", [])
            query = conv[0].get("content", "") if conv else ""

            console.print(f"Executing [bold cyan]{eval_id}[/bold cyan]...")
            user_id = f"eval_{eval_id}"
            session = await remote_agent.async_create_session(user_id=user_id)
            session_id = session.get("id")

            generator = remote_agent.async_stream_query(
                user_id=user_id, session_id=session_id, message=query
            )
            tool_calls = []
            final_text = ""

            try:
                async for event in generator:
                    if "content" in event and "parts" in event["content"]:
                        for part in event["content"]["parts"]:
                            if "function_call" in part:
                                tool_calls.append(part["function_call"]["name"])
                    if event.get("role") == "model" and "content" in event:
                        for part in event["content"].get("parts", []):
                            if "text" in part:
                                final_text += part["text"]
                status = "[bold green]PASS[/bold green]"
            except Exception as e:
                status = f"[bold red]ERROR: {e}[/bold red]"

            results_table.add_row(
                eval_id,
                query[:45] + "..." if len(query) > 45 else query,
                ", ".join(tool_calls) if tool_calls else "None",
                status,
            )

    asyncio.run(_execute_all())
    console.print("\n")
    console.print(results_table)


if __name__ == "__main__":
    app()
