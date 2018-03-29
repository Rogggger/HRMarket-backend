#  coding: utf-8
import datetime

from flask_login import login_required, current_user
from sqlalchemy import and_
from flask import Blueprint, request
from marshmallow import Schema, fields

from app.model.data_collection import DataCollection
from app.model.report_time import ReportTime
from app.model.user import User
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.serializer.notice import NoticeParaSchema
from app.view import bp_admin
from app.model.notice import Notice


@bp_admin.route("/notification", methods=["POST"])
@login_required
def notification_manage():  # 管理员设定通知

    json = request.get_json()
    data, errors = NoticeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001)
    now = datetime.datetime.now()
    data['created_at'] = now
    data['source'] = '山东省人力资源管理部门'
    data['user_id'] = current_user.id
    new_data = Notice(**data)
    session.add(new_data)
    session.commit()
    return jsonify({})


@bp_admin.route("/notification", methods=["GET"])
@login_required
def notification_get():  # 管理员获得他设定的通知

    res = Notice.query.filter_by(user_id=current_user.id).all()
    data_need, errors = NoticeParaSchema(many=True).dump(res)
    if errors:
        return error_jsonify(10000001)
    return jsonify(data_need)


@bp_admin.route("/<int:id>/notification", methods=["POST"])
@login_required
def notice_manage_id(id):  # 更改管理员获得的通知
    json = request.get_json()
    data, errors = NoticeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001)

    data_need = Notice.query.filter_by(id=id)
    if data_need.first() is None:
        return error_jsonify(10000001)

    data_need.update(data)
    session.commit()
    return jsonify({})


@bp_admin.route("/<int:id>/notification", methods=["DELETE"])
@login_required
def notice_manage_delete(id):  # 删除id对应的通知

    data_need = Notice.query.filter_by(id=id).first()
    if data_need is None:
        return error_jsonify(10000001)

    session.delete(data_need)
    session.commit()
    return jsonify({})
