from rest_framework import serializers
from .models import *
import chatting_django.settings as settings
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
	sender_url = serializers.SerializerMethodField()
	group_name = serializers.SerializerMethodField()

	def get_sender_url(self, obj):
		return (obj.sender.profile_image.image)

	def get_group_name(self, obj):
		if obj.group is not None:
			return (obj.group.name)
		return None

	class Meta:
		model = Message
		fields = '__all__'


class GroupUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id',)


class GroupSerializer(serializers.ModelSerializer):
	# users = GroupUserSerializer(read_only=True, many=True)

	class Meta:
		model = Group
		fields = '__all__'
