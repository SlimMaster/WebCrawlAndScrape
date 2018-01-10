from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
#from django.core.context_processors import csrf

# Create your views here.
@csrf_protect
def login(request):
	c = {}
	c.update(request)

	return render(request,'login.html')


def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')

	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')

def loggedin(request):
	return render('loggedin.html',{'full_name': request.user.username})



def invalid_login(request):
	return render(request,'invalid_login.html')

def logout(request):
	auth.logout(request)
	return render(request,'logout.html')

def home_view(request):

	return render(request,'base.html')
