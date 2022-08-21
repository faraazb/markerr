import logging
from flask import Blueprint, jsonify, request, g, current_app
from sqlalchemy import or_
from wtforms import Form, StringField, FormField, FieldList
from wtforms.validators import InputRequired
from markerr.models.annotation import Element, TextHighlight
from markerr.models.comment import Comment
from markerr.models.site import Page, SitePermissions
from supertokens_python.recipe.session.framework.flask import verify_session

log = logging.getLogger(__name__)


class TextHighlightForm(Form):
    color = StringField(validators=[InputRequired()])
    content = StringField(validators=[InputRequired()])


class ElementForm(Form):
    element = StringField()
    css_selector = StringField(validators=[InputRequired()])
    xpath = StringField(validators=[InputRequired()])
    text_highlights = FieldList(FormField(TextHighlightForm))


class CommentForm(Form):
    # heading = StringField(validators=[InputRequired()])
    content = StringField(validators=[InputRequired()])
    # use validators=[DataRequired()] to require elements
    elements = FieldList(FormField(ElementForm))
    team_id = StringField()
    reply_to_id = StringField()
    parent_id = StringField()


comments = Blueprint("comments", __name__, url_prefix="/comments")
"""
Comment Routes

+---------+--------------------------------------------------+---------------------------+
| Method  | Rule                                             | Description               |
+=========+==================================================+===========================+
| GET     | /comments/<uuid:page_id>                         | get all root comments     |
+---------+--------------------------------------------------+---------------------------+
| GET     | /comments/<uuid:page_id>/<uuid:root_comment_id>  | get a discussion          |
+---------+--------------------------------------------------+---------------------------+
| POST    | /comments/<uuid:page_id>                         | post a comment on a page  |
+---------+--------------------------------------------------+---------------------------+
| PUT     | /comments/<uuid:comment_id>                      | update a comment          |
+---------+--------------------------------------------------+---------------------------+
| DELETE  | /comments/<uuid:comment_id>                      | delete a comment          |
+---------+--------------------------------------------------+---------------------------+

- a discussion consists of all replies to a root comment

"""


@comments.route("/<uuid:page_id>", methods=["GET"])
@comments.route("/<uuid:page_id>/<uuid:root_comment_id>", methods=["GET"])
def get(page_id, root_comment_id=None):
    """
    For a page, get root comments or all replies to the root comment

    1. get the site from Page
    2. If public read_comments, return all is_public and ALL team comments
    3. If private read_comments, only if site owner, return all comments
    4. If teams read_comments, get Page.site.teams intersection user.teams.
        Return comments belonging to intersected teams and is_public comments

    :param page_id: page_id of the page
    :param root_comment_id: root comment of which to get the reply comments
    :return: list of root comments
    """
    page = Page.query.get(page_id)
    if not page:
        return jsonify({
            "status": "fail",
            "message": "Invalid page_id. This page does not exist."
        }), 400

    # query filters
    filters = []

    # we first get all the session_handles (List[string]) for a user

    if g.user is None:
        # if site private
        if page.site.permission_read_comments == SitePermissions.private:
            return jsonify({
                "status": "fail",
                "message": "not allowed"
            }), 403
        elif page.site.permission_read_comments == SitePermissions.teams:
            # if teams or public, return only public comments
            filters.append(Comment.team_id == None)
    else:
        # if private read access, ensure site ownership
        if page.site.permission_read_comments == SitePermissions.private:
            if not page.site.owner == g.user:
                return jsonify({
                    "status": "fail",
                    "message": "not allowed"
                }), 403
        elif page.site.permission_read_comments == SitePermissions.teams:
            # if teams, return all comments that belong to teams
            # the user is a member of and public comments
            # TODO should we instead do the below op. with ids?
            allowed_teams = list(set(page.site.allowed_teams) & set(g.user.teams))
            # in_() not yet supported for relationships
            # also in_([t.id for t in allowed_teams] + [None]) doesn't work
            filters.append(or_(
                Comment.team_id.in_([t.id for t in allowed_teams]),
                Comment.team_id == None
            ))
    # NOTE is operator (parent_id is None) doesn't work with query filters
    items = Comment.query.order_by(Comment.updated.desc()).filter(
        Comment.page_id == page_id,
        Comment.parent_id == root_comment_id,
        Comment.is_deleted == False,
        *filters
    ).all()
    return jsonify({"status": "success", "data": [item.serialize for item in items]})


@comments.route("/<uuid:page_id>", methods=["POST"])
@verify_session()
def post(page_id):
    """
    Create a comment on a page
    :param page_id:
    :return: The comment created
    """
    # TODO Maybe convert this into a decorator
    page = Page.query.get(page_id)
    if not page:
        return jsonify({"status": "fail", "message": "Invalid page_id. Page does not exist."}), 400

    form = CommentForm.from_json(request.json)
    # log.info(form)
    if not form.validate():
        return jsonify({"status": "fail", "data": form.errors, "message": "Form field errors"})
    # Now use form.<field>.data to create a model
    comment = Comment(
        user_id=g.user.id,
        page_id=page_id,
        # heading=form.heading.data,
        content=form.content.data,
        parent_id=form.parent_id.data,
        reply_to_id=form.reply_to_id.data,
        team_id=form.team_id.data
    )
    for e in form.elements.data:
        # highlights = []
        element = Element(
            element=e["element"],
            css_selector=e["css_selector"],
            xpath=e["xpath"]
        )
        comment.elements.append(element)
        # comment.elements.append(e)
        for h in e["text_highlights"]:
            element.text_highlights.append(
                TextHighlight(element_id=element.id, color=h["color"], content=h["content"])
            )
    # comment.elements = elements
    current_app.session.add(comment)
    current_app.session.commit()
    return jsonify({"status": "success", "data": comment.serialize}), 200


@comments.route("/<uuid:comment_id>", methods=["PUT"])
@verify_session()
def put(comment_id):
    """
    Update a comment

    :param comment_id: id of the comment to update
    :return: updated comment
    """
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"status": "fail", "message": "Invalid comment_id. Comment does not exist."}), 400
    if not comment.user_id == g.user.id:
        return jsonify({"status": "fail", "message": "not allowed"}), 403

    form = CommentForm.from_json(request.json)
    # log.info(form)
    if not form.validate():
        return jsonify({"status": "fail", "data": form.errors, "message": "Form field errors"})

    comment.heading = form.heading.data,
    comment.content = form.content.data,
    comment.parent_id = form.parent_id.data,
    comment.reply_to_id = form.reply_to_id.data,
    comment.team_id = form.team_id.data

    # reset comment elements
    comment.elements = []
    # add new elements
    for e in form.elements.data:
        # highlights = []
        element = Element(
            element=e["element"],
            css_selector=e["css_path"],
            xpath=e["xpath"]
        )
        comment.elements.append(element)
        # comment.elements.append(e)
        for h in e["text_highlights"]:
            element.text_highlights.append(
                TextHighlight(element_id=element.id, color=h["color"], content=h["content"])
            )

    current_app.session.commit()
    return jsonify({"status": "success", "data": {"comment": comment.serialize}}), 200


@comments.route("/<uuid:comment_id>", methods=["DELETE"])
@verify_session()
def delete(comment_id):
    # one_or_none will raise an exception if multiple comments found, which is not possible
    comment = Comment.query.filter(Comment.id == comment_id, Comment.is_deleted == False).one_or_none()
    if not comment:
        return jsonify({"status": "fail", "message": "Invalid comment_id. Comment does not exist."}), 400
    comment.is_deleted = True
    current_app.session.commit()
    return jsonify({"status": "success"}), 200
