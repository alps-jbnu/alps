import pathlib

from click import group, option, Path

from .app import app, initialize_app
from .config import read_config

__all__ = 'main',


@group()
def main():
    pass


@main.command()
@option('--debug', '-d', is_flag=True)
@option('--port', '-p', type=int)
@option('--config', '-c', type=Path(exists=True))
def runserver(debug, port, config):
    """서버를 실행합니다."""

    config_dict = read_config(pathlib.Path(config))
    initialize_app(app=app, config_dict=config_dict)
    app.run(debug=debug, port=port)
