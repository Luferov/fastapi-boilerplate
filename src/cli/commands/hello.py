from src.cli.utils import typer_async


@typer_async
async def hello_command(name: str) -> None:
    print(f'Hello, {name}')
