# coding: utf-8

from flask import Blueprint, request
from flask_login import login_required, current_user
from sqlalchemy import exc
from marshmallow import Schema, fields, post_load, pre_dump
from app.model.event import Event
from app.model.label import Label
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.consts import (
    InvalidArguments,
    SyncError
)

bp_sync = Blueprint('sync', __name__, url_prefix='/sync')


class LabelSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    color = fields.Integer(required=True)
    last_modified = fields.DateTime(required=True, format='iso')
    status = fields.Integer(required=True)


class EventSchema(Schema):
    id = fields.Integer(required=True)
    label_id = fields.Integer(required=True)
    task = fields.String(required=True)
    note = fields.String(required=True)
    deadline = fields.DateTime(required=True, format='iso')
    reminders = fields.String(required=True)
    last_modified = fields.DateTime(required=True, format='iso')
    status = fields.Integer(required=True)

    @post_load
    def activity_post_load(self, data):
        if data['label_id'] == 0:
            data['label_id'] = None
        return data

    @pre_dump
    def activity_pre_dump(self, obj):
        if obj.label_id is None:
            obj.label_id = 0
        return obj


class SyncSchema(Schema):
    labels = fields.List(fields.Nested(LabelSchema), required=True)
    label_sync_threshold = fields.DateTime(required=True)
    events = fields.List(fields.Nested(EventSchema), required=True)
    event_sync_threshold = fields.DateTime(required=True)


def do_sync(new_list, threshold, type):
    """
    通用的同步函数，首先遍历传入的new，如果本地没有对应的id就推到新建列表中，交给do_add新建。
    如果本地有id，要判断是本地的last_modified新还是传入的新，
    如果是本地新就将本地的添加到回传列表；如果是传入的新就更新本地。
    遍历之后，开始取出所有没处理过的、时间比阈值该用户的list新的，添加到回传列表
    :param new_list: 传入的list<list>
    :param threshold: 传入的阈值<datetime>
    :param type: 传入的list里的类型<'label'/'event'>
    :return: 回传列表<list>
    """
    data_type = {'label': Label, 'event': Event}
    add_list = list()
    update_list = list()
    change_list = list()
    passback_list = list()
    uid = current_user.id
    real_type = data_type[type]
    # 注意，传入的new_list中的对象是一个字典，而不是数据库对象
    if new_list:
        for x in new_list:
            xid = x['id']
            change_list.append(xid)
            local_x = session.query(real_type).filter(real_type.user_id == uid, real_type.id == xid).first()
            if local_x is None:
                add_list.append(x)
            else:
                if local_x.last_modified > x['last_modified']:
                    passback_list.append(local_x)
                else:
                    update_list.append(x)
    try:
        do_add(add_list, real_type)
    except exc.SQLAlchemyError:
        session.rollback()
        raise exc.SQLAlchemyError('Operation Insert Failed')

    try:
        do_update(update_list, real_type)
    except exc.SQLAlchemyError:
        session.rollback()
        raise exc.SQLAlchemyError('Operation Update Failed')
    else:
        session.commit()

    local_list = session.query(real_type).filter(real_type.user_id == uid, real_type.last_modified > threshold).all()
    if local_list:
        passback_list.extend([x for x in local_list if x.id not in change_list])
    passback_list = LabelSchema().dump(passback_list, many=True) if type == 'label' else EventSchema().dump(
        passback_list, many=True)
    return passback_list.data


def do_update(update_list, type):
    if update_list:
        for y in update_list:
            session.query(type).filter_by(id=y['id']).update(y)
        session.flush()


def do_add(add_list, type):
    if add_list:
        for y in add_list:
            # caution: y is a **dict** rather than a simple query object
            instance = type(**y)
            instance.user_id = current_user.id
            session.add(instance)
        session.flush()


@bp_sync.route('', methods=['POST'])
@login_required
def sync():
    """
    注册视图，只接受POST消息，根据发来的lable和event
    进行同步，参数不对返回400，同步失败返回401
    :return: HTTP状态码和json信息（客户端需要更新的对象信息）
    """
    json = request.get_json()
    data, errors = SyncSchema().load(json)
    if errors:
        return error_jsonify(InvalidArguments, errors, 400)
    new_labels = data['labels']
    new_events = data['events']
    label_sync_threshold = data['label_sync_threshold']
    event_sync_threshold = data['event_sync_threshold']

    # starting sync
    try:
        passback_labels = do_sync(new_list=new_labels, threshold=label_sync_threshold, type='label')
    except exc.SQLAlchemyError as e:
        return error_jsonify(SyncError, specifiy_error=e.message, status_code=401)
    try:
        passback_events = do_sync(new_list=new_events, threshold=event_sync_threshold, type='event')
    except exc.SQLAlchemyError as e:
        return error_jsonify(SyncError, specifiy_error=e.message, status_code=401)

    result = {
        'labels': passback_labels,
        'events': passback_events
    }
    return jsonify(result)
