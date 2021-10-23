from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json

from api.models import TeamFeeDetail
from api.serializer import TeamFeeDetailSerializer

class teamFeeDetailViewSet(viewsets.ModelViewSet):
    queryset = TeamFeeDetail.objects.all()
    serializer_class = TeamFeeDetailSerializer
    