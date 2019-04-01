from django.shortcuts import render,HttpResponse

# Create your views here.
def login(request):
    def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
            return HttpResponseRedirect('/home')
		else:
            return render(request, 'login.html', {'errors': False})

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/home')
		else:
			return render(request, 'login.html', {'errors': True})
