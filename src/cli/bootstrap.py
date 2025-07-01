import typer

from .commands.hello import hello_command


def create_app() -> typer.Typer:
    app = typer.Typer()

    app.command()(hello_command)

    return app
