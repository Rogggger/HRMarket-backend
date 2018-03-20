#  coding : utf-8
from sqlalchemy import Column, Integer, String, Sequence, TIMESTAMP
from app.libs.db import db


class notice(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)  # 标题
    body = Column(String(2000), nullable=False)  # 主体
    time = Column(TIMESTAMP, nullable=False)  # 时间
    souurce = Column(String(50), nullable=False)  # 发布单位
    user_id = Column(Integer, nullable=False)
