from rest_framework import serializers
from api.models import Requirement

# Create your models here.
class RequirementSerializer(serializers.Serializer):
    class Meta:
        model = Requirement
        fields = '__all__'