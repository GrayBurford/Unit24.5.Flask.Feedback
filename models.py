from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect our app to the database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Make model instance of User class"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="users", cascade="all, delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register new user with hashed password. Data sent from view route function to here, then password is hashed, and we return new instance of User at the end."""
        
        hashed_pwd = bcrypt.generate_password_hash(password)
        # now turn bytestring into normal (unicode utf8) string
        hashed_pwd_utf8 = hashed_pwd.decode('utf8')

        user = cls(
            username=username,
            password=hashed_pwd_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
            )
        db.session.add(user)
        return user

    @classmethod
    def authorize(cls, username, password):
        """Authorizes a user if username/password are correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Make model instance of Feedback class"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)