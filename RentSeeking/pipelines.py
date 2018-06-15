# -*- coding: utf-8 -*-
import time
from scrapy.exceptions import DropItem

from .items import ApmBaseInfoItem, AmpDetailInfoItem
from .models import load_session, create_table
from .models.model import ApmBaseInfo, ApmDetailInfo
from .models.record import Record
from pymysql.err import Error as PymsqlError


class RentseekingPipeline(object):
    def process_item(self, item, spider):
        for i in item.keys():
            if item[i]:
                item[i] = item[i].strip()
            else:
                item[i] = ''
        item['area'] = item['area'].replace('平米', '')
        item['area'] = item['area'].replace('㎡', '')
        if '-' in item['price']:
            low = int(item['price'].split('-')[0])
            high = int(item['price'].split('-')[1])
            item['price'] = str(int((low + high) / 2))
        if isinstance(item, ApmBaseInfoItem):
            item['subway'] = item['subway'].split('线')[0] + '线'
        if isinstance(item, AmpDetailInfoItem):
            item['apm_detail_url'] = item['apm_detail_url'].split('?')[0]
        if len(item['price']) == 1 or item['price'] == '':
            raise DropItem
        return item


class MysqlPipline(object):
    base_info_count = 0
    detail_info_count = 0

    def __init__(self):
        self.cost_time = 0

    def process_item(self, item, spider):

        create_table()

        if isinstance(item, ApmBaseInfoItem):
            self.apmbaseinfo(item, spider)
        if isinstance(item, AmpDetailInfoItem):
            self.ampdetailinfo(item, spider)
        return item

    def apmbaseinfo(self, item, spider):
        a = ApmBaseInfo(
            apm_name=item['apm_name'],
            apm_url=item['apm_url'],
            cell_name=item['cell_name'],
            cell_type=item['cell_type'],
            area=item['area'],
            built_year=item['built_year'],
            price=item['price'],
            subway=item['subway'],
            created_at=item['created_at'],
            updated_at=item['updated_at'],
            website=spider.name
        )
        session = load_session()
        try:
            session.merge(a)
            session.commit()
            self.base_info_count += 1
        except PymsqlError as e:
            print('Mysql Error: %s ' % str(e))

    def ampdetailinfo(self, item, spider):
        a = ApmDetailInfo(
            apm_name=item['apm_name'],
            price=item['price'],
            area=item['area'],
            floor=item['floor'],
            apm_detail_url=item['apm_detail_url'],
            traffication=item['traffication'],
            location=item['location'],
            cell_type=item['cell_type'],
            orientation=item['orientation'],
            contact=item['contact'],
            contact_identity=item['contact_identity'],
            phone=item['phone'],
            created_at=item['created_at'],
            updated_at=item['updated_at'],
            website=spider.name
        )
        session = load_session()
        try:
            session.merge(a)
            session.commit()
            self.detail_info_count += 1
        except PymsqlError as e:
            print('Mysql Error: %s ' % str(e))

    def close_spider(self, spider):
        r = Record(
            base_info_count=self.base_info_count,
            detail_info_count=self.detail_info_count,
            spider=spider.name,
            cost_time=(time.time()-self.cost_time)
        )
        session = load_session()
        session.merge(r)
        session.commit()

    def open_spider(self, spider):
        self.cost_time = time.time()
