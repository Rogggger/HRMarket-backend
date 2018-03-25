# coding: utf-8
from flask import Blueprint, request

from flask_login import login_required, current_user

from app.model.corporate_Info import Info
from app.serializer.info import InfoParaSchema
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.consts import (
    InvalidArguments,
    GetInfoError
)

# 企业本身数据填报
bp_info = Blueprint("info", __name__, url_prefix="/info")


@bp_info.route("/record", methods=['POST'])
@login_required
def info_record():
    json = request.get_json()
    data, errors = InfoParaSchema().load(json)

    if errors:
        return error_jsonify(InvalidArguments, errors, 400)
    else:
        data['user_id'] = current_user.id
        tmp_info = Info.query.filter_by(user_id=current_user.id).first()
        if tmp_info:
            tmp_info.update(**data)
        else:
            new_info = Info(**data)
            session.add(new_info)
            session.commit()
        return jsonify({})


@bp_info.route("/record", methods=['GET'])
@login_required
def info_get():
    cur_id = current_user.id
    if Info.is_exist(cur_id):
        tmp_info = Info.query.filter_by(user_id=cur_id).first()
        json, error = InfoParaSchema().dump(tmp_info)
        return jsonify(json)
    else:
        return error_jsonify(GetInfoError, status_code=400)
