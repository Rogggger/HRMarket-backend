from sqlalchemy import Column, Integer, String, Sequence, TIMESTAMP
from app.libs.db import db


class DataCollection(db.Model):
    id = Column(Integer, Sequence('data_id'), primary_key=True, autoincrement=True)
    filing = Column(Integer, nullable=False)  # 初次建档时就业人数
    check = Column(Integer, nullable=False)  # 本次调查期就业人数
    otherreason = Column(String(55), nullable=False)  # 其他原因
    decreasetype = Column(String(50), nullable=True)  # 就业人数减少类型
    mainreason = Column(String(50), nullable=True)  # 主要原因
    mainreasondetail = Column(String(100), nullable=True)  # 主要原因说明
    secondreason = Column(String(50), nullable=True)  # 次要原因
    secondreasondetail = Column(String(100), nullable=True)  # 次要原因说明
    thirdreason = Column(String(50), nullable=True)  # 第三原因
    thirdreasondetail = Column(String(100), nullable=True)  # 第三原因
    time = Column(TIMESTAMP, nullable=False, default='0000-00-00 00:00:00')  # 填报时间
    status = Column(Integer, nullable=False)  # 状态，1为审查通过，0为未通过
    user_id = Column(Integer, nullable=False)  # 用户id

    @classmethod
    def is_exist(cls, user_id):
        res = cls.query.filter_by(user_id=user_id).all()
        if res:
            return True
        else:
            return False

