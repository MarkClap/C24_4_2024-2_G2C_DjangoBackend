from rest_framework import serializers
from .models import Users, Roles, UserRoles

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name']

class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = UserRoles
        fields = ['id', 'user', 'role']

class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

class RemoveRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email','password']
