from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.conf import settings
import json
import requests
import logging
from api import hjUtil
from api.hjConstant import DBErrorConst

from api.models import User, UserSession
from api.serializer import UserSerializer, UserSessionSerializer

logger = logging.getLogger('swallow')

class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = hjUtil.HJPageNumberPagination

    @action(detail=False, url_path='login')
    def onLogin(self, request, pk=None):
        logger.info('onLogin()')
        result = hjUtil.HJResponse()
        session = requests.session()
        payload = {
            "appid": settings.WX_GLOBAL.get('appId'),
            "secret": settings.WX_GLOBAL.get('appSecret'),
            "js_code": request.GET.get('data'),
            "grant_type": "authorization_code"
        }
        url = settings.WX_GLOBAL.get('wxServer') + 'jscode2session'
        res = session.get(url, params=payload)
        if "openid" in res.json():
            try:
                serializer = self.get_serializer(data={"userOpenId": res.json()["openid"], "userSessionCode": request.GET.get('data'), "userSessionKey": res.json()["session_key"]})
                serializer.is_valid(raise_exception=True)
                createdUser = self.perform_create(serializer)
            except ValidationError as ve:
                if 'userOpenId' in ve.args[0]:
                    self.lookup_field = 'userOpenId'
                    instance = User.objects.get(userOpenId=res.json()["openid"])
                    serializer = self.get_serializer(instance, data={"userSessionCode": request.GET.get('data'), "userSessionKey": res.json()["session_key"]}, partial=True)
                    logger.debug(serializer)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    result.setStatus(status.HTTP_200_OK)
                else:
                    logger.error(ve.args)
            except Exception as e:
                logger.error(e.args)
                result.setCode(DBErrorConst.G_DB_ERROR)
                result.setStatus(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                result.setData(res.json())
            return Response(result.getResult(), result.getStatus())
        else:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)