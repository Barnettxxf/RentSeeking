# -*- coding:utf-8 -*-
"""
author = Barnett
"""
import datetime

from . import Base
from sqlalchemy import Column, String, Integer, DateTime, Sequence


class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, Sequence('id', start=0, increment=1), primary_key=True)
    base_info_count = Column(Integer, nullable=False)
    detail_info_count = Column(Integer, nullable=False)
    spider = Column(String(255), nullable=False)
    cost_time = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, base_info_count, detail_info_count, spider, cost_time):
        self.base_info_count = base_info_count
        self.detail_info_count = detail_info_count
        self.spider = spider
        self.cost_time = cost_time
        self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
