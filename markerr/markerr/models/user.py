from markerr.db import Base
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from markerr.db.mixins import Timestamps


class User(Base, Timestamps):
    """Model class to represent a user"""

    __tablename__ = "users"

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    email = sa.Column(sa.Text, nullable=False)
    supertoken_id = sa.Column(pg.CHAR(length=36), nullable=False)
    username = sa.Column(sa.String(100), nullable=False)
    full_name = sa.Column(sa.Text)
    short_name = sa.Column(sa.Text)

    teams = sa.orm.relationship("Team", secondary="team_memberships", back_populates="members")
    """Teams of which the user is a `member`"""

    # TODO This is mostly not required, most users will not be leaders
    # These teams will also be present in ``teams`` which can be determined
    # with team.owner_id == user.id
    # owned_teams = sa.orm.relationship("Team", back_populates="users")
    """Teams of which the user is the `creator`"""

    sites = sa.orm.relationship("Site", back_populates="owner")
    """Sites owned by the user"""

    def __str__(self):
        return f"{self.id} {self.full_name}"

    def serialize(self, only_profile=False):
        # TODO Send teams and sites - need to add serialize on those models
        # IDK why str(self.id: UUID) is needed. Probably bc Supertoken's
        # jsonify implementation doesn't handle UUIDs
        serialized = {
            "id": str(self.id),
            "username": self.username,
            "short_name": self.short_name,
            "full_name": self.full_name
        }
        if not only_profile:
            serialized["email"] = self.email
            # serialized["teams"] = [team.serialize for team in self.teams]
            # serialized["sites"] = [site.serialize for site in self.sites]
        return serialized
