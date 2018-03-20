from flask_login import login_required, current_user
from app.model.corporateInfo import Info
from flask import Blueprint, request, flash
from marshmallow import Schema, fields
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.consts import (
    InvalidArguments,
    GetInfoError
)

bp_info = Blueprint("info", __name__, url_prefix="/info")


class InfoParaSchema(Schema):
    area = fields.String(50)  # 所属地区
    code = fields.String(20)  # 组织机构代码
    name = fields.String(55)  # 企业名称
    nature = fields.String(50)  # 企业性质
    belong_to = fields.String(50)  # 所属行业
    main_business = fields.String(55)  # 主营业务
    contacts = fields.String(55)  # 联系人
    address = fields.String(55)  # 联系地址
    postal_code = fields.String(55)  # 邮政编码
    phone = fields.String(55)  # 联系电话
    fax = fields.String(55)  # 传真
    email = fields.String(50)  # email


@bp_info.route("/record", methods=['POST'])
@login_required
def info_record():
    json = request.get_json()
    data, errors = InfoParaSchema().load(json)

    if errors:
        return error_jsonify(InvalidArguments, errors, 400)
    else:
        data['user_id'] = current_user.id
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
        return error_jsonify(GetInfoError, specifiy_error="Can not get the info", status_code=400)
