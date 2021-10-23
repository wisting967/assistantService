import django_filters
from api.models import *

class TeamFilter(django_filters.rest_framework.FilterSet):
    def filter_queryset(self, queryset):
        return queryset.filter(teamStatus='Active')

    class Meta:
        models = Team
        fields = ("__all__")