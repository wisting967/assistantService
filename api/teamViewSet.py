from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
import json
import logging

from api import hjUtil, hjConstant
from api.hjConstant import DBErrorConst, UserErrorConst, GeneralErrorConst
from api.models import User, Team
from api.serializer import TeamSerializer
from api.filter import TeamFilter

logger = logging.getLogger('swallow')

class teamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = hjUtil.HJPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, )
    filter_class = TeamFilter

    @action(detail=False, url_path='getTeamList')
    def onGetTeamList(self, request, pk=None):
        logger.info('onGetTeamList()')
        result = hjUtil.HJResponse()
        teamList = []
        try:
            for team in self.queryset.filter(teamOwner=User.objects.get(userSessionCode=request.GET.get("data")).userOpenId):
                teamList.append(team.teamName)
        except User.DoesNotExist as e:
            result.setCode = UserErrorConst.G_USER_NOLOGIN
            result.setStatus = 400
        except Exception as e:
            result.setCode = GeneralErrorConst.G_ERROR_UNKNOW
            result.setStatus = 500
        
        result.setData(teamList)
        return Response(result.getResult(), result.getStatus())
    