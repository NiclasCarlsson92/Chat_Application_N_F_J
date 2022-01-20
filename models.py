from app import db


# Primary key to identify a unique....
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.BOOLEAN, default=False)
