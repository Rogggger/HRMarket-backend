# coding: utf-8
from sqlalchemy import Column, Integer, String, Sequence, TIMESTAMP
from app.libs.db import db


# 记录数据填报时间段
class ReportTime(db.Model):
    id = Column(Integer, Sequence('time_id'), primary_key=True, autoincrement=True)
    start_time = Column(TIMESTAMP, nullable=False)  # 填报开始时间
    end_time = Column(TIMESTAMP, nullable=False)  # 填报结束时间
    user_id = Column(Integer, nullable=False)  # 此填报时间创始人
