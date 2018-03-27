#  coding: utf-8
import datetime

from flask_login import login_required, current_user

from flask import Blueprint, request
from marshmallow import Schema, fields

from app.model.data_collection import DataCollection
from app.model.report_time import ReportTime
from app.model.user import User
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.serializer.data import DataParaSchema

# 企业数据填报
bp_data = Blueprint("data", __name__, url_prefix="/data")


class DataGetParaSchema(Schema):
    start = fields.DateTime()  # 结束时间
    end = fields.DateTime()  # 开始时间


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
        can_find_time_range = 0  # 能否确定时间段标志
        admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
        report_time = ReportTime.query.filter_by(user_id=admin_user.id).all()  # 找到省级管理员设置的提交时间
        for tmp_time in report_time:
            if tmp_time.start_time <= now <= tmp_time.end_time:  # 确定当前时间的时间段,默认只有一个符合
                can_find_time_range = 1
                tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=tmp_time.id)
                # 找到企业填报的符合条件的数据
                if tmp_data:  # 修改企业条目，并保存
                    tmp_data.update(data)
                    session.commit()
                    break
                else:  # 新建一个企业填报条目，并保存
                    data['time_id'] = tmp_time.id
                    data['status'] = 0
                    data['user_id'] = current_user.id
                    new_data = DataCollection(**data)
                    session.add(new_data)
                    session.commit()
                    break
        if can_find_time_range == 0:  # 现在不在任何可以填报的时间段内
            return error_jsonify(10000014)
        return jsonify({})


@bp_data.route("/record", methods=['GET'])
@login_required
def info_record_get():
    now = datetime.datetime.now()
    can_find_time_range = 0  # 能否确定时间段标志
    admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
    report_time = ReportTime.query.filter_by(user_id=admin_user.id).all()  # 找到省级管理员设置的提交时间
    for tmp_time in report_time:
        if tmp_time.start_time <= now <= tmp_time.end_time:  # 确定当前时间的时间段,默认只有一个符合
            can_find_time_range = 1
            tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=tmp_time.id).first()
            # 找到企业填报的符合条件的数据
            if tmp_data:
                data_need, errors = DataParaSchema().dump(tmp_data)
                return jsonify(data_need)
    if can_find_time_range == 0:  # 现在不在任何可以填报的时间段内
        return error_jsonify(10000014)


@bp_data.route("/report", methods=['POST'])
@login_required
def info_report():
    json = request.get_json()
    data, errors = DataParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)
    else:
        now = datetime.datetime.now()
        data['time'] = now
        can_find_time_range = 0  # 能否确定时间段标志
        admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
        report_time = ReportTime.query.filter_by(user_id=admin_user.id).all()  # 找到省级管理员设置的提交时间
        for tmp_time in report_time:
            if tmp_time.start_time <= now <= tmp_time.end_time:  # 确定当前时间的时间段,默认只有一个符合
                can_find_time_range = 1
                tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=tmp_time.id)
                # 找到企业填报的符合条件的数据
                if tmp_data:  # 修改企业条目，并上报
                    data['status'] = 1
                    tmp_data.update(data)
                    session.commit()
                    break
                else:  # 没有找到，说明信息没有保存
                    return error_jsonify(10000015)
        if can_find_time_range == 0:  # 现在不在任何可以填报的时间段内
            return error_jsonify(10000014)
        return jsonify({})


@bp_data.route("/get", methods=['GET', 'POST'])
@login_required
def info_get():
    json = request.get_json()
    data, errors = DataGetParaSchema().load(json)
    if errors:
        return error_jsonify(10000001)

    tmp_data = DataCollection.query.filter_by(user_id=current_user.id).all()
    res = []
    for i in tmp_data:
        if data['start'] <= i.time <= data['end']:
            data_need, errors = DataParaSchema().dump(i)
            res.append(data_need)
    return jsonify(res)
