from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, TIMESTAMP, Boolean

from app.libs.db import db


class Label(db.Model):
    id = Column(Integer, Sequence('label_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    color = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    last_modified = Column(TIMESTAMP(timezone=True))
    status = Column(Integer, nullable=False)
