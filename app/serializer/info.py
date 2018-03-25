# coding: utf-8
from marshmallow import Schema, fields, post_load, pre_dump


class InfoParaSchema(Schema):
    address = fields.List(fields.String(5))  # 联系地址
    address_detail = fields.String(55)  # 联系地址详细
    area = fields.String(50)  # 所属地区
    belong_to = fields.List(fields.String(50))  # 所属行业
    code = fields.String(20)  # 组织机构代码
    contacts = fields.String(55)  # 联系人
    email = fields.String(50)  # email
    enterprise_kind = fields.String(10)  # 企业类型
    enterprise_scale = fields.String(10)  # 企业规模
    fax = fields.String(55)  # 传真
    main_business = fields.String(55)  # 主营业务
    name = fields.String(55)  # 企业名称
    phone = fields.String(55)  # 联系电话
    postal_code = fields.String(55)  # 邮政编码

    @post_load
    def compose(self, data):
        address = '/'.join(data.pop('address'))
        data['address'] = '{}/{}'.format(address, data.pop('address_detail'))
        data['enterprise'] = "{}/{}".format(data.pop('enterprise_kind'), data.pop('enterprise_scale'))
        data['belong_to'] = '/'.join(data['belong_to'])

    @pre_dump
    def decompose(self, obj):
        address1, address2, detail = obj.address.split('/')
        obj.address = [address1, address2]
        obj.address_detail = detail
        kind, scale = obj.enterprise.split('/')
        obj.enterprise_kind = kind
        obj.enterprise_scale = scale
        obj.belong_to = obj.belong_to.split('/')
