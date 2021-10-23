from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json

from api.models import TeamFee
from api.serializer import TeamFeeSerializer
from api import hjUtil

class teamFeeViewSet(viewsets.ModelViewSet):
    queryset = TeamFee.objects.all()
    serializer_class = TeamFeeSerializer
    pagination_class = hjUtil.HJPageNumberPagination
    