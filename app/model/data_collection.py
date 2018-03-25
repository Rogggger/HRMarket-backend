# coding: utf-8
from sqlalchemy import Column, Integer, String, Sequence,TIMESTAMP
from app.libs.db import db


class DataCollection(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    employed_num = Column(Integer, nullable=False)  # 初次建档时就业人数
    employed_num_now = Column(Integer, nullable=False)  # 本次调查期就业人数
    other_reason = Column(String(55), nullable=False)  # 其他原因
    _type = Column(String(50), nullable=True)  # 就业人数减少类型
    main_reason = Column(String(50), nullable=True)  # 主要原因
    main_reason_explan = Column(String(100), nullable=True)  # 主要原因说明
    second_reason = Column(String(50), nullable=True)  # 次要原因
    second_reason_explan = Column(String(100), nullable=True)  # 次要原因说明
    third_reason = Column(String(50), nullable=True)  # 第三原因
    third_reason_explan = Column(String(100), nullable=True)  # 第三原因
    time= Column(TIMESTAMP,nullable=False) # 填报时间
    status= Column(Integer,nullable=False) # 状态，1为审查通过，0为未通过
    user_id=Column(Integer,nullable=False)  # 用户id

