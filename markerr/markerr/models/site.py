import enum
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from markerr.db import Base, mixins


class SitePermissions(enum.Enum):
    """
    Permissions for a :py:class:`Site`
    """
    public = "public"
    private = "private"
    teams = "teams"


class Site(Base, mixins.Timestamps):
    """
    Model class representing a website
    """
    __tablename__ = "sites"

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    owner_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("users.id"))
    owner = sa.orm.relationship("User", back_populates="sites")

    # TODO - Validation for name and url
    name = sa.Column(sa.Text, nullable=False, unique=True)
    display_name = sa.Column(sa.Text)

    pages = sa.orm.relationship("Page", back_populates="site")

    permission_read_comments = sa.Column(
        sa.Enum(SitePermissions, name="site_permission_read_comment"),
        server_default=SitePermissions.public.value,
        nullable=False,
    )
    permission_write_comments = sa.Column(
        sa.Enum(SitePermissions), name="site_permission_write_comment",
        server_default=SitePermissions.public.value,
        nullable=False,
    )

    # TODO NOTE
    # Remember to not directly access site.allowed_teams without checking permissions first
    # make something clever to do it automatically, or simply set/reset allowed_teams whenever
    # permission changes
    allowed_teams = sa.orm.relationship("Team", secondary="team_sites", back_populates="sites")
    """Teams allowed to read and write comments when permission_(read|write)_comments is set to ``teams``"""


class Page(Base, mixins.Timestamps):
    """
    Model class representing a page of a website
    """
    __tablename__ = "pages"

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())

    url = sa.Column(sa.Text, nullable=False, unique=True)

    site_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("sites.id"))
    site = sa.orm.relationship("Site", back_populates="pages")




