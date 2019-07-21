from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class testView(APIView):
    
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