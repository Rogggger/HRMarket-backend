from flask_login import login_required, current_user
from app.model.data_collection import DataCollection
from flask import Blueprint, request
from marshmallow import Schema, fields
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
import datetime
from app.consts import (
    InvalidArguments,
    GetInfoError
)

# 企业数据填报

bp_data = Blueprint("data", __name__, url_prefix="/data")


class DataParaSchema(Schema):
    filing = fields.Integer(10)  # 初次建档时就业人数
    check = fields.Integer(10)  # 本次调查期就业人数
    otherreason = fields.String(55)  # 其他原因
    decreasetype = fields.String(50)  # 就业人数减少类型
    mainreason = fields.String(50)  # 主要原因
    mainreasondetail = fields.String(100)  # 主要原因说明
    secondreason = fields.String(50)  # 次要原因
    secondreasondetail = fields.String(100)  # 次要原因说明
    thirdreason = fields.String(50)  # 第三原因
    thirdreasondetail = fields.String(100)  # 第三原因


@bp_data.route("/record", methods=['POST'])
@login_required
def info_record():
    json = request.get_json()
    data, errors = DataParaSchema().load(json)

    if errors:
        return error_jsonify(InvalidArguments, errors, 400)
    else:
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        data['time'] = now
        data['status'] = 0
        data['user_id'] = current_user.id
        new_data = DataCollection(**data)
        session.add(new_data)
        session.commit()
        return jsonify({})


@bp_data.route("/record", methods=['GET'])
@login_required
def info_get():
    cur_id = current_user.id
    if DataCollection.is_exist(cur_id):
        tmp_data = DataCollection.query.filter_by(user_id=cur_id).first()
        json, error = DataParaSchema().dump(tmp_data)
        return jsonify(json)
    else:
        return error_jsonify(GetInfoError, specifiy_error="Can not get the info", status_code=400)
