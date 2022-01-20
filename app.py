from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Many parts of flask will require use of a secret key, therefor we create one.
    app.config['SECRET_KEY'] = '123secret'

    # Configuring SQLAlchemy to use SQLite and the file db.sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize SQLAlchemy object with our app object
    db.init_app(app)

    from blueprints.home import bp_home
    app.register_blueprint(bp_home)

    from blueprints.signup import bp_signup
    app.register_blueprint(bp_signup)

    from blueprints.login import bp_login
    app.register_blueprint(bp_login)

    return app
