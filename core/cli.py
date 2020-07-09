import click
from flask.cli import with_appcontext
from flask import current_app as app

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    app.logger.info('Drop database')
    app.db.drop_all()

@click.command("init-db")
@click.option("--quiet", "-q", is_flag=True)
@with_appcontext
def init_db_command(quiet):
    """Initialize application database"""
    if not quiet:
        print("Initialize database...", end='', flush=True)
    app.logger.info('Initialize database')
    db = app.db
    db.create_all()
    if not quiet:
        print("done", flush=True)

@click.command("seed-beer")
@click.option("--quiet", "-q", is_flag=True)
@with_appcontext
def seed_beer_command(quiet):
    """Seed beer table(s)"""
    if not quiet:
        print("Seed beers...", end='', flush=True)
    from beers.database.models import Beer
    Beer.seed()
    if not quiet:
        print("done", flush=True)

commands = [init_db_command,drop_db_command,seed_beer_command]
