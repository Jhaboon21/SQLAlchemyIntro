import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMG = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"



"""Models for Blogly."""
class User(db.Model):
    """User."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    first_name = db.Column(db.String(15),
                           nullable=False)
    
    last_name = db.Column(db.String(15),
                          nullable=False)
    
    image_url = db.Column(db.Text, 
                          nullable=False, 
                          default=DEFAULT_IMG)
    
    posts = db.relationship("Post", backref="user")
    
    def __repr__(self):
        u = self
        return f"<id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Post."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False)

    content = db.Column(db.Text, 
                        nullable=False)

    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.Text, 
                     nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags",
    )
    
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)