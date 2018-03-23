# coding: utf-8

from flask import Blueprint, request
from flask_login import login_required, login_user, logout_user, current_user
from marshmallow import Schema, fields
from app.model.user import User
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.consts import (
    InvalidArguments,
    AccountAlreadyExist, AccountDoesNotExist,
    PasswordIsNotCorrect
)

bp_account = Blueprint('account', __name__, url_prefix='/account')


class AccountParaSchema(Schema):
    email = fields.String(required=True)
    password_md5 = fields.String(required=True)


@bp_account.route('/register', methods=['POST'])
# @login_required
def register():
    """
    注册视图，只接受POST消息，根据发来的用户名和密码
    进行注册，参数不对返回400，如果账户已有的话返回401
    :return: HTTP状态码和json信息
    """
    json = request.get_json()
    data, errors = AccountParaSchema().load(json)
    if errors:
        return error_jsonify(InvalidArguments, errors, 400)

    username = data['email']
    password_md5 = data['password_md5']
    if User.is_exist(username):
        return error_jsonify(AccountAlreadyExist, specifiy_error="Account already exist", status_code=400)
    else:
        if current_user.isAdmin == 1:  # 1 是市级，可以创建普通
            is_admin = 0
        elif current_user.isAdmin == 2:  # 2 省级，可以创建市级
            is_admin = 1

    new_user = User(name=username, password=password_md5, isAdmin=is_admin)
    session.add(new_user)
    session.commit()
    return jsonify({})


@bp_account.route('/login', methods=['POST'])
def login():
    """
    最基本的登录视图，只能通过post发送登录信息
    如果发送的参数不对返回400，用户不存在和密码错误返回401，
    :return: HTTP状态码和json信息
    """
    json = request.get_json()
    data, errors = AccountParaSchema().load(json)
    if errors:
        return error_jsonify(InvalidArguments, errors, 400)

    username = data['email']
    password_md5 = data['password_md5']
    attempt_user = User.query.filter_by(name=username).first()
    if attempt_user is None:
        return error_jsonify(AccountDoesNotExist, specifiy_error="Account does not exist", status_code=400)
    else:
        if attempt_user.has_right_password(password_md5):
            login_user(attempt_user)
            return jsonify({"is_admin": attempt_user.isAdmin})
        else:
            return error_jsonify(PasswordIsNotCorrect, specifiy_error="password is not correct", status_code=400)


@bp_account.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({})
