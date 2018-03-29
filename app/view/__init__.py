from flask import Blueprint

bp_admin = Blueprint("admin", __name__, url_prefix="/admin")

from app.view.user import admin_time_manage
from app.view.user import admin_notification_manage
