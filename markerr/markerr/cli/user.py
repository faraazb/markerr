import logging

import click
from flask.cli import with_appcontext
from supertokens_python.syncio import delete_user

log = logging.getLogger(__name__)


@click.command("supertoken-delete")
@click.option("-i", "--i", required=True)
@with_appcontext
def delete_supertoken_user(i):
    log.info(f"deleting user: {i}")
    delete_user(i)
