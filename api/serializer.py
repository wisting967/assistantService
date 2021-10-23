from rest_framework import serializers
from api.models import User, UserSession, Requirement, Team, TeamFee, TeamMember, TeamFeeDetail

# Create your models here.
class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ('__all__')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class TeamFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFee
        fields = '__all__'

class TeamFeeDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(TeamFeeDetailSerializer, self).to_representation(instance)
        if data['feeDetailType']:
            data['feeDetailType'] = '+'
        else:
            data['feeDetailType'] = '-'
        return data
    class Meta:
        model = TeamFeeDetail
        fields = '__all__'