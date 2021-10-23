from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json

from api.models import Requirement
from api.serializer import RequirementSerializer

class requirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    