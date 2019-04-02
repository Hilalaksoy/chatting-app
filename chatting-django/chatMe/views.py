from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.template.defaulttags import register
from django.contrib.auth.models import User

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
        email=request.POST['email']
        password=request.POST['password']

        newUser=User(username=username,email=email)
        newUser.set_password(password)

        newUser.save()
        return render(request, 'login.html')


@method_decorator(login_required, name='dispatch')
class MainPage(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'main.html', {'herhangi_bir_parametre': None})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
