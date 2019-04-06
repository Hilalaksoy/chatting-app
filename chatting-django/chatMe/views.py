from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.template.defaulttags import register
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from .utils import *
import json

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

class Login(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html', {'errors': False})

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html', {'errors': True})

class Register(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'register.html')

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		if len(User.objects.filter(username=username)) != 0:
			return render(request, 'register.html', {'errors': 'Bu kullanıcı adı alınmıştır. Başka bir ad seçiniz.' })

		newUser = User(username=username,email=email)
		newUser.set_password(password)
		newUser.save()
		profile_image, created =  UserProfileImage.objects.get_or_create(user=newUser)
		profile_image.image = gravatar_url(email)
		profile_image.user = newUser
		profile_image.save()

		ChatmeBroadcaster, created = User.objects.get_or_create(username='ChatMe', email='chat@me.com')
		if created:
			ChatmeBroadcaster.set_password('chatmeee')
			chatme_image, created =  UserProfileImage.objects.get_or_create(user=ChatmeBroadcaster)
			chatme_image.image = gravatar_url('chat@me.com')
			chatme_image.user = ChatmeBroadcaster
			chatme_image.save()

		Message.objects.create(sender=ChatmeBroadcaster, receiver=newUser,type=Message.SINGLE_USER, content=
		'Hoş geldiniz, burası herkesin ulaşabileceği bir mesajlaşma alanıdır. Lütfen duyarlı kullanınız.')

		return render(request, 'login.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class MainPage(View):
	def get(self, request, *args, **kwargs):
		current_user = request.user
		sent_messages = Message.objects.filter(sender=current_user)
		received_messages = Message.objects.filter(receiver=current_user)
		chats_dic = {}

		for message in sent_messages:
			if message.receiver not in chats_dic.keys():
				chats_dic[message.receiver] = []
			chats_dic[message.receiver].append(message)

		for message in received_messages:
			if message.sender not in chats_dic.keys():
				chats_dic[message.sender] = []
			chats_dic[message.sender].append(message)

		for chat in chats_dic.values():
			chat.sort(key=lambda mes: mes.date)

		chats_set = [ (chatter, chat) for chatter, chat in chats_dic.items() ]
		chats_set.sort(key=lambda tup: tup[1][-1].date, reverse=True )

		token, created = Token.objects.get_or_create(user=current_user)
		context = {
			'current_user': current_user,
			'chats_set': chats_set,
			'token': token
			}
		return render(request, 'main.html', context)
