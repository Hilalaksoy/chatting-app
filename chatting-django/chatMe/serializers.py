from rest_framework import serializers
from .models import *
import chatting_django.settings as settings

class MessageSerializer(serializers.ModelSerializer):
	sender_url = serializers.SerializerMethodField()

	def get_sender_url(self, obj):
		return (obj.sender.profile_image.image)

	def get_receiver_url(self, obj):
		return (obj.receiver.profile_image.image)

	class Meta:
		model = Message
		fields = '__all__'
