import configparser
import os
import pathlib
import subprocess

from click import argument, group, option, Path

from alps.app import app, initialize_app
from alps.config import read_config

__all__ = 'main',


@group()
def main():
    pass


@main.command()
@option('--debug', '-d', is_flag=True)
@option('--port', '-p', type=int)
@option('--config', '-c', type=Path(exists=True))
def runserver(debug, port, config):
    """Run ALPS server"""

    if config:
        config_dict = read_config(pathlib.Path(config))
        initialize_app(app=app, config_dict=config_dict)
    app.run(debug=debug, port=port)


@main.command()
@argument('config', type=Path(exists=True))
@argument('alembic-command')
def migration(config, alembic_command):
    """Run Alembic command with sqlalchemy_url in configuration file,
    not depending on the sqlalchemy_url in alembic.ini file

    Example:

    .. code-block:: console

        $ alps migration example.cfg.yml "alembic revision \
          --autogenerate -m 'Added account table'"
        $ alps migration example.cfg.yml "alembic upgrade head"
    """

    # Load configuration file and alembic.ini
    if not config:
        print('Require config filename')
        return

    config_dict = read_config(pathlib.Path(config))
    if not config_dict.get('DATABASE_URL'):
        print('Require DATABASE_URL in config')
        return

    config_parser = configparser.ConfigParser()
    config_parser.read(os.path.join(os.path.dirname(__file__), 'alembic.ini'))

    # Backup current working directory and the ini file
    working_dir = os.getcwd()
    alembic_dir = os.path.dirname(__file__)
    ini_path = os.path.join(alembic_dir, 'alembic.ini')
    ini_backup_path = os.path.join(alembic_dir, 'alembic.ini.backup')

    # Change working directory to the ini directory
    os.chdir(alembic_dir)
    os.rename(ini_path, ini_backup_path)
    with open(ini_path, 'w') as alembic_config_file:
        config_parser['alembic']['sqlalchemy.url'] = \
            config_dict['DATABASE_URL']
        config_parser.write(alembic_config_file)

    # Call Alembic command
    subprocess.call(alembic_command, shell=True)

    # Restore alembic.ini and change working directory to initial directory
    os.rename(ini_backup_path, ini_path)
    os.chdir(working_dir)
