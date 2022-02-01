import dotenv

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '123secret'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.filter_by(id=user_id).first()

    from blueprints.home import bp_home
    app.register_blueprint(bp_home)

    from blueprints.signup import bp_signup
    app.register_blueprint(bp_signup)

    from blueprints.signin import bp_signin
    app.register_blueprint(bp_signin)

    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    from blueprints.dashboard import bp_dashboard
    app.register_blueprint(bp_dashboard)

    from blueprints.chatroom import bp_chatroom
    app.register_blueprint(bp_chatroom)

    from blueprints.dm import bp_dm
    app.register_blueprint(bp_dm)

    from blueprints.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1.0') # Ska alltid ha /api/version prefix

    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    return app


if __name__ == '__main__':
    dotenv.load_dotenv()
    app = create_app()
    app.run()
