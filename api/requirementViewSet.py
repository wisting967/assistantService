from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json

from api.models import Requirement

class requirementViewSet(viewsets.ViewSet):
    queryset = Requirement.objects.all()
    
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #get_arg1 = request.GET.get('arg1', None)
        #get_arg2 = request.GET.get('arg2', None)

        # Any URL parameters get passed in **kw
        #result = myClass.do_work()
        resList = []
        resList.append({"name":"tom", "age": 21, "sex": "male"})
        resList.append({"name":"jerry", "age": 20, "sex": "female"})

        response = Response(resList, status=status.HTTP_200_OK)
        return response
    
    # list() 方法必须重写，否则会导致url(xxxxxxx/prefix/) 返回404
    def list(self, request):
        print('list')
        return Response('abc', status=status.HTTP_200_OK)
    