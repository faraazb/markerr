import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from markerr.db import Base


# class AnnotationElements(Base):
#     """
#     Association table for annotations and elements
#     """
#     __tablename__ = "annotation_elements"
#
#     __table_args__ = (sa.UniqueConstraint("annotation_id", "element_id", name="unique_annotation_element"), )
#
#     id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
#     annotation_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("annotations.id"))
#     element_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("elements.id"))
#
#
# class Annotation(Base):
#     """
#     Model class representing an Annotation
#     """
#     __tablename__ = "annotations"
#
#     id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
#
#     elements = sa.orm.relationship("Element", secondary="annotation_elements")


class Element(Base):
    """
    Model class proxying an HTML element
    """
    __tablename__ = "elements"

    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    comment_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("comments.id"), nullable=False)
    element = sa.Column(sa.Text)
    css_selector = sa.Column(sa.Text)
    xpath = sa.Column(sa.Text)

    # has_text_highlights = sa.Column(sa.Boolean, default=False, nullable=False)
    text_highlights = sa.orm.relationship("TextHighlight")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "element": self.element,
            "css_selector": self.css_selector,
            "xpath": self.xpath,
            "text_highlights": [highlight.serialize for highlight in self.text_highlights]
        }


class TextHighlight(Base):
    """
    Model class representing a text highlight in an ``Element``
    """
    __tablename__ = "text_highlights"
    id = sa.Column(pg.UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v4())
    # TODO How to store highlight color? Req. being able to extend with multiple/custom colors
    color = sa.Column(sa.Text)

    element_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("elements.id"), nullable=False)

    content = sa.Column(sa.UnicodeText, nullable=False)
    """The highlighted text"""

    @property
    def serialize(self):
        return {
            "id": self.id,
            "color": self.color,
            "content": self.content
        }


