import logging
import click
from flask import current_app
from flask.cli import with_appcontext
from markerr import db
from markerr.models.comment import Comment
from markerr.models.user import User


log = logging.getLogger(__name__)


@click.command("initdb")
@with_appcontext
def initdb():
    log.info("initializing database")
    # get engine bounded to session
    engine = current_app.session.get_bind()
    db.init(engine, drop_all=True, create_all=True)


@click.command("testdb")
@with_appcontext
def test_command():
    comments = Comment.query.all()
    for comment in comments:
        log.info(comment)
        # log.info(comment.parent)
        # log.info(comment.reply_to)
        log.info(comment.replies)
        log.info("BREAK")



