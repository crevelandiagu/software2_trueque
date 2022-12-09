from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, abort
)

from flask_login import login_required, current_user
from app.database import db
from app.domain.auth.models import User
from app.domain.blogs.forms import PostForm
from app.domain.blogs.models import Comment, Post

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
def index():
    posts = Post.query.join(
        User, Post.author_id == User.id
    ).add_columns(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username
    ).order_by(
        Post.created.desc()
    ).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        for comment in form.comments:
            comment = Comment(body=comment.body.data, post_id=post.id)
            db.session.add(comment)

        db.session.commit()
        return redirect(url_for('blog.index'))

    comments_in_json = [ 
        dict([('body', comment.body.data if comment.body.data else ''), ('errors', list(comment.body.errors))])
        for comment in form.comments
    ]

    return render_template('blog/form.html', form = form, comments_in_json = comments_in_json)


def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    form = PostForm()

    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    if request.method == 'POST' and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()

        return redirect(url_for('blog.index'))

    comments_in_json = [ 
        # dict([('body', comment.body.data if comment.body.data else ''), ('errors', list(comment.body.errors))])
        # for comment in form.comments
    ]

    return render_template('blog/form.html', form=form, comments_in_json=comments_in_json, hide_comments=True)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))