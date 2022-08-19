import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from markerr.db import Base, mixins


class TeamSites(Base):
    """
    Association table for teams and sites
    """
    __tablename__ = "team_sites"
    __table_args__ = (sa.UniqueConstraint("site_id", "team_id", name="unique_team_site"),)

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    team_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("teams.id"))
    site_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("sites.id"))


class TeamMembership(Base):
    """
    Association table for teams and users
    """
    __tablename__ = "team_memberships"

    __table_args__ = (sa.UniqueConstraint("user_id", "team_id"), )

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    user_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False)
    team_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("teams.id"), nullable=False)


class Team(Base, mixins.Timestamps):
    __tablename__ = "teams"

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    owner_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("users.id"))
    owner = sa.orm.relationship("User")

    # TODO validation for name and description
    name = sa.Column(sa.UnicodeText, nullable=False)
    description = sa.Column(sa.UnicodeText, nullable=False)

    members = sa.orm.relationship("User", secondary="team_memberships", back_populates="teams")

    sites = sa.orm.relationship("Site", secondary="team_sites", back_populates="allowed_teams")
