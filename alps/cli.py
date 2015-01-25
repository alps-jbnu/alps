import configparser
import os
import pathlib
import subprocess

from click import argument, group, option, Path

from alps.app import app, initialize_app
from alps.config import read_config
from alps.db import Base, get_engine
from alps.dummy import insert_dummy_data
from alps.model import import_all_modules

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
@argument('database-url')
@argument('alembic-command')
def migration(database_url, alembic_command):
    """Run Alembic command with database url argument,
    not depending on the sqlalchemy_url in alembic.ini file

    Example:

    .. code-block:: console

        $ alps migration postgresql:///alps "alembic revision \
          --autogenerate -m 'Added account table'"
        $ alps migration postgresql:///alps "alembic upgrade head"
    """

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
        config_parser['alembic']['sqlalchemy.url'] = database_url
        config_parser.write(alembic_config_file)

    # Call Alembic command
    subprocess.call(alembic_command, shell=True)

    # Restore alembic.ini and change working directory to initial directory
    os.rename(ini_backup_path, ini_path)
    os.chdir(working_dir)


@main.command()
@option('--config', '-c', type=Path(exists=True))
@option('--database-url', '-d', type=str)
def schema(config, database_url):
    """Create all of the tables from Metadata.
    If tables exist before run this command, they will be dropped.
    """

    if config:
        config_dict = read_config(pathlib.Path(config))
        initialize_app(app=app, config_dict=config_dict)

    if not database_url:
        database_url = None

    with app.app_context():
        import_all_modules()
        engine = get_engine(database_url=database_url)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)


@main.command()
@option('--config', '-c', type=Path(exists=True))
def dummy(config):
    """Insert dummy data for testing purpose.
    Preassumed the DB revision is in head and there are no duplicate records
    for dummy data.
    """

    if config:
        config_dict = read_config(pathlib.Path(config))
        initialize_app(app=app, config_dict=config_dict)

    insert_dummy_data(app)
