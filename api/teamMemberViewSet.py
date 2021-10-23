from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json

from api.models import TeamMember
from api.serializer import TeamMemberSerializer

class teamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    