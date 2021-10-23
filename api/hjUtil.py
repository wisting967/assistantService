import logging
from django.conf import settings
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger('swallow')

class HJPageNumberPagination(PageNumberPagination):
    # 默认每页显示的数据条数（不指定limit的时候）
    page_size = 10
    # 在URL用limit=xx可以自定义每页显示的数据条数
    page_size_query_param = 'limit'
    # 每页最大显示的条数（指定limit的条数大于该值时，该值生效）
    max_page_size = 200
    # URL中page=xx，返回第几页的数据
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'code': "0",
            'count': self.page.paginator.count,
            'data': data
        })

class HJResponse():
    def __init__(self):
        self.result = {}
        self.result['code'] = '0'
        self.result['msg'] = ''
        self.status = 200

    def setCode(self, code):
        self.result['code'] = code

    def getCode(self):
        return self.result.get('code')

    def setMsg(self, msg):
        self.result['msg'] = msg

    def getMsg(self):
        return self.result.get('msg')

    def setData(self, data):
        self.result['data'] = data

    def getData(self):
        if self.result.get('data'):
            return self.result.get('data')
        else:
            return ''

    def setCount(self, count):
        self.result.setdefault('count', count)

    def getCount(self):
        if self.result.get('count'):
            return self.result.get('count')
        else:
            return 0

    def getResult(self):
        return self.result

    def setStatus(self, status):
        self.status = status
    
    def getStatus(self):
        return self.status
    
