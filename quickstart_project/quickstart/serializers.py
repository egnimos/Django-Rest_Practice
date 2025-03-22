from django.contrib.auth.models import User, Group
from rest_framework import serializers

# serializer is used to serialize/structure the raw data comming or outgoing from the API
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
