# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from forms import RegisterForm
from forms import LoginForm
from django.core.context_processors import csrf
from models import RegisteredUsers
from django.shortcuts import render
from django.http import HttpResponseRedirect
from auth import login
from auth import islogin
from auth import logout
def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegisterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #Add users to db 
            user = RegisteredUsers()
            try:
                user.email = form.cleaned_data["reg_emailid"]
                user.pswd = form.cleaned_data["reg_pswd"]
                user.name = form.cleaned_data["reg_name"]
                user.bloodgroup = form.cleaned_data["reg_bloodgroup"]
                user.dob = form.cleaned_data["reg_dob"]
                user.dolbd = form.cleaned_data["reg_dolbd"]
                user.sex = form.cleaned_data["reg_sex"]
                user.mobile = form.cleaned_data["reg_mobile"]
                user.hidemob = form.cleaned_data["reg_hidemob"]
                user.city = form.cleaned_data["reg_city"]
                user.save()
            except:
                return HttpResponse("Error in Connection with Database , Try again "+str(vars(user)))
            return HttpResponse("validation sucessfull and regsiterd .. Redirecting ..")
            #return HttpResponseRedirect('/registered/') # Redirect after POST
        else:
            c={}
            c.update(csrf(request))
            c.update({"form":form})
            c.update({"test":"testing"})
            c.update({"reg":True})
            #return HttpResponse("validation failed because "+str(c))
            return render_to_response('index.html',c)
    c = {}
    c.update({"reg":True})
    c.update(csrf(request))
    return render_to_response('index.html',c)

def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            log_emailid = form.cleaned_data["log_emailid"]
            login(request,log_emailid)
            return render_to_response('profile.html')
#            return HttpResponse("Logged In success")
        else:
            c={}
            c.update(csrf(request))
            c.update({"form":form})
            return render_to_response('index.html',c)
    if(islogin(request)):
        logout(request)
        return HttpResponse("Already Logined")
        
    c = {} 
    c.update(csrf(request))
    return render_to_response('index.html',c)

def search(request):
    return render_to_response('search.html')

def profile(request):
    if(islogin(request)):
        return render_to_response('profile.html')
    else:
        c = {} 
        c.update(csrf(request))
        return render_to_response('index.html',c)