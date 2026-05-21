"""Terminal UI components powered by Rich and Colorama."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterable

from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

init(autoreset=True)


class TerminalUI:
    """Professional-grade terminal interface helper."""

    def __init__(self) -> None:
        self.console = Console()

    def banner(self, title: str, subtitle: str) -> None:
        self.console.print(
            Panel.fit(
                f"[bold cyan]{title}[/bold cyan]\n[white]{subtitle}[/white]",
                title="AI Framework",
                border_style="bright_blue",
            )
        )

    def info(self, message: str) -> None:
        self.console.print(f"[bold green]INFO:[/bold green] {message}")

    def warning(self, message: str) -> None:
        self.console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")

    def error(self, message: str) -> None:
        self.console.print(f"[bold red]ERROR:[/bold red] {message}")

    def ask(self, prompt: str) -> str:
        return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL} ").strip()

    def show_menu(self, title: str, options: Iterable[str]) -> None:
        table = Table(title=title, title_style="bold magenta")
        table.add_column("Option", justify="right", style="cyan", no_wrap=True)
        table.add_column("Action", style="white")
        for index, option in enumerate(options, start=1):
            table.add_row(str(index), option)
        self.console.print(table)

    @contextmanager
    def spinner(self, text: str):
        with self.console.status(f"[bold green]{text}[/bold green]", spinner="dots"):
            yield

    def panel(self, title: str, body: str, style: str = "blue") -> None:
        self.console.print(Panel(body, title=title, border_style=style))

