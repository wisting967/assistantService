from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from api import test, requirementViewSet

router = routers.DefaultRouter()
router.register(r'req', requirementViewSet.requirementViewSet)

urlpatterns = [
    url(r'^a/', include(router.urls)),
    # url(r'^test/', test.testView.as_view()),
]
