from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from api import test, requirementViewSet, userViewSet, teamViewSet, teamMemberViewSet, teamFeeViewSet, teamFeeDetailViewSet

router = routers.DefaultRouter()
router.register(r'req', requirementViewSet.requirementViewSet, base_name='req')
router.register(r'user', userViewSet.userViewSet, base_name='user')
router.register(r'team', teamViewSet.teamViewSet, base_name='team')
router.register(r'teammember', teamMemberViewSet.teamMemberViewSet, base_name='teammember')
router.register(r'teamfee', teamFeeViewSet.teamFeeViewSet, base_name='teamfee')
router.register(r'teamfeedetail', teamFeeDetailViewSet.teamFeeDetailViewSet, base_name='teamfeedetail')

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    # url(r'^test/', test.testView.as_view()),
]
