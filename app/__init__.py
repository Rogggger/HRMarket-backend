from flask import Flask
from app.libs.login import login_manager
from app.libs.db import db
from app.view.user.helloworld import bp_hello_world
from app.view.user.account import bp_account
from app.view.user.sync import bp_sync
from app.view.user.info_record import bp_info
from app.view.user.data_record import bp_data


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(bp_hello_world)
    app.register_blueprint(bp_account)
    app.register_blueprint(bp_sync)
    app.register_blueprint(bp_info)
    app.register_blueprint(bp_data)

    login_manager.init_app(app)
    db.init_app(app)

    from app.model.user import User
    from app.model.label import Label
    from app.model.event import Event

    return app
