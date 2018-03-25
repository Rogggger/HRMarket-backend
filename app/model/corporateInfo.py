#  coding : utf-8
from sqlalchemy import Column, Integer, String, Sequence
from app.libs.db import db


class Info(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    area = Column(String(50), nullable=False)  # 所属地区
    code = Column(String(20), nullable=False)  # 组织机构代码
    name = Column(String(55), nullable=False)  # 企业名称
    enterprise_scale = Column(Integer, nullable=False)  # 企业规模，
    enterprise_kind = Column(Integer, nullable=False)  # 企业经济类型
    belong_to_1 = Column(String(5), nullable=False)  # 所属行业1,大类
    belong_to_2 = Column(String(5), nullable=False)  # 所属行业2，内部分类
    main_business = Column(String(50), nullable=False)  # 主营业务
    contacts = Column(String(50), nullable=False)  # 联系人
    address_1 = Column(String(50), nullable=False)  # 联系地址下拉菜单1
    address_2 = Column(String(50), nullable=False)  # 联系地址下拉菜单2
    postal_code = Column(String(6), nullable=False)  # 邮政编码
    phone = Column(String(15), nullable=False)  # 联系电话
    fax = Column(String(12), nullable=False)  # 传真
    email = Column(String(50), nullable=True)  # email
    user_id = Column(Integer, nullable=False)

    @classmethod
    def is_exist(cls,user_id):
        res = cls.query.filter_by(user_id=user_id).all()
        if res:
            return True
        else:
            return False

