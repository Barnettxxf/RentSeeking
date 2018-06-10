# -*- coding:utf-8 -*-
"""
author = Barnett
"""

from . import Base
from sqlalchemy import Column, String, Integer, DateTime, Sequence, Text


class ApmBaseInfo(Base):
    __tablename__ = 'baseinfo'

    id = Column(Integer, Sequence('id', start=0, increment=1), primary_key=True)
    apm_name = Column(String(255), nullable=False)
    apm_url = Column(Text, nullable=False)
    cell_name = Column(String(255), nullable=True)
    cell_type = Column(String(255), nullable=False)
    area = Column(String(255), nullable=True)
    built_year = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)
    subway = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, apm_name, apm_url, cell_name, cell_type, area, built_year, price, subway, created_at,
                 updated_at):
        self.apm_name = apm_name
        self.apm_url = apm_url
        self.cell_name = cell_name
        self.cell_type = cell_type
        self.area = area
        self.built_year = built_year
        self.price = price
        self.subway = subway
        self.created_at = created_at
        self.updated_at = updated_at


class ApmDetailInfo(Base):
    __tablename__ = 'detailinfo'

    id = Column(Integer, Sequence('id', start=0, increment=1), primary_key=True)
    apm_name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    area = Column(String(255), nullable=True)
    floor = Column(String(255), nullable=True)
    apm_detail_url = Column(String(255), nullable=True)
    traffication = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    cell_type = Column(String(255), nullable=False)
    orientation = Column(String(255), nullable=True)
    contact = Column(String(255), nullable=False)
    contact_identity = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, apm_name, price, area, floor, apm_detail_url,
                 traffication, location, cell_type, orientation,contact,
                 contact_identity, phone, created_at, updated_at):
        self.apm_name = apm_name
        self.price = price
        self.area = area
        self.floor = floor
        self.apm_detail_url = apm_detail_url
        self.traffication = traffication
        self.location = location
        self.cell_type = cell_type
        self.orientation = orientation
        self.contact = contact
        self.contact_identity = contact_identity
        self.phone = phone
        self.created_at = created_at
        self.updated_at = updated_at
