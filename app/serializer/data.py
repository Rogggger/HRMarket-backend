# coding: utf-8
from marshmallow import Schema, fields


class DataParaSchema(Schema):
    filing = fields.Integer()  # 初次建档时就业人数
    check = fields.Integer()  # 本次调查期就业人数
    other_reason = fields.String(55)  # 其他原因
    decrease_type = fields.String(50)  # 就业人数减少类型
    main_reason = fields.String(50)  # 主要原因
    main_reason_detail = fields.String(100)  # 主要原因说明
    second_reason = fields.String(50)  # 次要原因
    second_reason_detail = fields.String(100)  # 次要原因说明
    third_reason = fields.String(50)  # 第三原因
    third_reason_detail = fields.String(100)  # 第三原因
    status = fields.Integer()  # 状态
