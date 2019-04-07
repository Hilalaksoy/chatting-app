from rest_framework import serializers, viewsets, permissions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser,MultiPartParser
from django.contrib.auth import authenticate, login
from django.core.files import File
from uuid import UUID, uuid4
from .models import *
from .serializers import *
from .utils import *
import json
import base64

from django.contrib.auth.models import User

class ChatViewSet(viewsets.ModelViewSet):
	queryset = Message.objects.filter(id=-1)
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = MessageSerializer
	parser_classes = (MultiPartParser, JSONParser)

	def get_queryset(self):
		try:
			id = int(self.request.GET['id'])
		except:
			param = self.request.GET.get('id', '')
			if param != '' and param[0] == 'G':
				return get_group_chat(int(param[1:]))
			elif param == 'server':
				return Message.objects.filter(type='A').order_by('date')
			else:
				return []

		if len(User.objects.filter(id=id)) == 0:
			return []
		return get_chat(self.request.user, User.objects.filter(id=id).first())


class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = GroupSerializer
	parser_classes = (MultiPartParser, JSONParser)


class ValidateToken(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def post(self, request, *args, **kwargs):
		token = ''
		user_id = None
		try:
			token = request.data.get('token', '')
			user_id = int(request.data.get('user_id', -1))

		except:
			return Response({
				'valid': False
			})
		if len(Token.objects.filter(user=user_id, key=token)) == 0:
			return Response({
				'valid': False
			})

		return Response({
			'valid': True
		})
