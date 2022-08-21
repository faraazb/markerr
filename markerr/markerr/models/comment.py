from sqlalchemy import Sequence

from markerr.db import Base, mixins
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


DISPLAY_SEQ = Sequence("comments_display_id_seq", start=1)


class Comment(Base, mixins.Timestamps):
    """
    Model class to represent a comment

    TODO Need to decide how to use Comment.is_public,
        right now it's disregarded, but it can be used to support
        a feature wherein read_access PUBLIC can only read is_public.
        Rn, we dont need is_public because once site is set to PUBLIC,
        all comments can be read anyway
        In one way, PUBLIC is a special team consisting of everyone,
        and PRIVATE is a special team consisting of only site owner
        ---
        08/08
        Got rid of is_public, team_id == None indicates public comment.
        When PUBLIC, anyone can read all comments.
        When TEAM, team members can read team+public comments and anyone
        can read only public comments
    """

    __tablename__ = "comments"
    # TODO: indexing
    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())

    display_id = sa.Column(sa.Integer, DISPLAY_SEQ, server_default=DISPLAY_SEQ.next_value())
    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)

    is_resolved = sa.Column(sa.Boolean, default=False, nullable=False)

    # heading = sa.Column(sa.UnicodeText)
    content = sa.Column(sa.UnicodeText, nullable=False)

    user_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False)
    user = sa.orm.relationship("User")

    page_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("pages.id"), nullable=False)
    page = sa.orm.relationship("Page")

    elements = sa.orm.relationship("Element")
    """Annotated elements"""

    team_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("teams.id"))
    team = sa.orm.relationship("Team")

    reply_to_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("comments.id"))
    """Comment to which this comment is an immediate (depth = 1) reply"""
    # reply_to = sa.orm.relationship("Comment", foreign_keys=[reply_to_id], remote_side=[id], back_populates="replies")
    # immediate_replies = sa.orm.relationship("Comment", foreign_keys=[reply_to_id], back_populates="reply_to")
    # """Immediate replies to this comment (Not really required I think)"""

    parent_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("comments.id"))
    """Root comment"""
    # parent = sa.orm.relationship("Comment", foreign_keys=[parent_id], remote_side=[id], back_populates="replies")

    replies = sa.orm.relationship("Comment", foreign_keys=[parent_id])
    """`All` replies to the comment"""

    def __str__(self):
        # TODO Better string repr
        return f"{self.id} {self.content}"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "display_id": self.display_id,
            "is_resolved": self.is_resolved,
            "created": self.created,
            "updated": self.updated,
            "user": self.user.serialize(only_profile=True),
            "reply_to_id": self.reply_to_id,
            "parent_id": self.parent_id,
            "content": self.content,
            "elements": [element.serialize for element in self.elements],
            "is_deleted": self.is_deleted
        }