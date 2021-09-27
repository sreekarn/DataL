import config
import logging

from flask import Flask, request as req

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()

def init_app(config):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from .models import User
        from app.controllers import pages, resources, auth
        
        app.register_blueprint(pages.blueprint)
        app.register_blueprint(resources.blueprint)
        app.register_blueprint(auth.blueprint)
        db.create_all()  # Create sql tables for our data models

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        return app
