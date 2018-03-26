#  coding: utf-8
import datetime

from flask_login import login_required, current_user

from flask import Blueprint, request

from app.model.data_collection import DataCollection
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.serializer.data import DataParaSchema

# 企业数据填报
bp_data = Blueprint("data", __name__, url_prefix="/data")


@bp_data.route("/record", methods=['POST'])
@login_required
def info_record():
    json = request.get_json()
    data, errors = DataParaSchema().load(json)

    if errors:
        return error_jsonify(10000001, errors)
    else:
        now = datetime.datetime.now()
        data['time'] = now
        data['status'] = 0
        data['user_id'] = current_user.id
        try:
            new_data = DataCollection(**data)
            session.add(new_data)
        except Exception:
            session.rollback()
            return error_jsonify(10000002)
        else:
            session.commit()
        return jsonify({})


@bp_data.route("/record", methods=['GET'])
@login_required
def info_get():
    cur_id = current_user.id
    tmp_data = DataCollection.query.filter_by(user_id=cur_id).first()
    if tmp_data is None:
        tmp_data = {}
    json, error = DataParaSchema().dump(tmp_data)
    if error:
        return error_jsonify(10000002)
    return jsonify(json)
