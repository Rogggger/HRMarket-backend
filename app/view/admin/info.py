#  coding: utf-8

from flask_login import login_required
from flask import request, Blueprint
from app.model.corporate_Info import Info
from app.serializer.info import InfoParaSchema, InfoSearchSchema
from app.decorator.auth import admin_required
from app.libs.http import error_jsonify, jsonify

# 数据汇总
bp_admin_info = Blueprint('admin_info', __name__, url_prefix='/admin/info')


@bp_admin_info.route("/", methods=["POST"])
@login_required
@admin_required
def get_info():
    json = request.get_json()
    data, errors = InfoSearchSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)
    area = u'%{}%'.format(data.get('area'))
    infos = Info.query.filter(Info.area.like(area)).all()
    json = InfoParaSchema(many=True).dump(infos)
    return jsonify(json)
