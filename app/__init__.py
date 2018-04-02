from flask import Flask
from app.libs.login import login_manager
from app.libs.db import db
from app.view.user.helloworld import bp_hello_world
from app.view.user.account import bp_account
from app.view.user.info_record import bp_info
from app.view.user.data_record import bp_data
from app.view.user.notification import bp_notification
from app.view.admin.notification_manage import bp_admin_notification
from app.view.admin.time_manage import bp_admin_time
from app.view.admin.summary import bp_admin_summary
from app.view.admin.datacheck import bp_admin_data_check


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(bp_hello_world)
    app.register_blueprint(bp_account)
    app.register_blueprint(bp_info)
    app.register_blueprint(bp_data)
    app.register_blueprint(bp_notification)
    app.register_blueprint(bp_admin_notification)
    app.register_blueprint(bp_admin_time)
    app.register_blueprint(bp_admin_summary)
    app.register_blueprint(bp_admin_data_check)

    login_manager.init_app(app)
    db.init_app(app)

    return app
