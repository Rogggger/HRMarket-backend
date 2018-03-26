# coding: utf-8
from flask import Blueprint
from app.model.notice import Notice
from app.model.user import User
from flask_login import login_required, current_user
from app.serializer.notice import NoticeParaSchema
from app.libs.http import jsonify, error_jsonify
from app.consts import (
    GetInfoError
)

bp_notification = Blueprint("notification", __name__, url_prefix="/notification")


@bp_notification.route("/", methods=['GET'])
@login_required
def notification_get():
    flag = current_user.isAdmin
    no_info_flag = 1
    res = {}
    res['length'] = 0
    res['notification'] = []
    for tmp_is_admin in range(flag, 3):
        tmp_user_id_list = User.query.filter_by(isAdmin=tmp_is_admin).all()
        for tmp_user in tmp_user_id_list:
            if Notice.is_exist(tmp_user.id):
                no_info_flag = 0
                tmp_notice_list = Notice.query.filter_by(user_id=tmp_user.id).all()
                for i in tmp_notice_list:
                    tmp_notice, errors = NoticeParaSchema().dump(i)

                    res['length'] += 1
                    res['notification'].append(tmp_notice)

    if no_info_flag == 1:
        return error_jsonify(GetInfoError, status_code=400)
    else:
        return jsonify(res)
