#  coding : utf-8
from sqlalchemy import Column, Integer, String, Sequence
from app.libs.db import db


class Info(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    area = Column(String(50), nullable=False)     # 所属地区
    code = Column(String(20), nullable=False)    # 组织机构代码
    name = Column(String(55), nullable=False)   # 企业名称
    nature = Column(String(50), nullable=False)  # 企业性质
    belong_to = Column(String(50), nullable=False)  # 所属行业
    main_business = Column(String(55), nullable=False)  # 主营业务
    contacts = Column(String(55), nullable=False)  # 联系人
    address = Column(String(55), nullable=False)  # 联系地址
    postal_code = Column(String(55), nullable=False)  # 邮政编码
    phone = Column(String(55), nullable=False)  # 联系电话
    fax = Column(String(55), nullable=False)  # 传真
    email = Column(String(50), nullable=True)  # email
    user_id = Column(Integer,nullable=False)


