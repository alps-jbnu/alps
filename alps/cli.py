from click import group, option

from .app import app

__all__ = 'main',


@group()
def main():
    pass


@main.command()
@option('--debug', '-d', is_flag=True)
@option('--port', '-p', type=int)
def runserver(debug, port):
    app.run(debug=debug, port=port)
