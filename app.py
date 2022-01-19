from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from blueprints.home import bp_home
    app.register_blueprint(bp_home)

    from blueprints.signup import bp_signup
    app.register_blueprint(bp_signup)

    return app
