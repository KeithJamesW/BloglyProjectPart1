"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://stem.oregonstate.edu/sites/stem.oregonstate.edu/files/profile/Generic%20person%20icon_3.jpg"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
       

        return f"{self.first_name} {self.last_name}"


def connect_db(app):
  

    db.app = app
    db.init_app(app)