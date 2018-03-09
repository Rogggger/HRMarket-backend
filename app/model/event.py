#  coding : utf-8

from sqlalchemy import Column, Integer, String, TIMESTAMP, Sequence, ForeignKey, Boolean
from app.libs.db import db


class Event(db.Model):
    id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
    task = Column(String(50), nullable=False)
    note = Column(String(500))
    label_id = Column(Integer, ForeignKey('label.id'))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    deadline = Column(TIMESTAMP(timezone=True))
    reminders = Column(String(50))
    last_modified = Column(TIMESTAMP(timezone=True))
    status = Column(Integer, nullable=False)
