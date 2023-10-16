from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMG = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

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
    
    def __repr__(self):
        u = self
        return f"<id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
