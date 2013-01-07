# Create your views here.
from django.http import HttpResponse, HttpResponseRedirectBase
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from forms import RegisterForm
from forms import LoginForm
from forms import SearchForm
from forms import ProfileForm
from django.core.context_processors import csrf
from models import RegisteredUsers
from django.shortcuts import render
from auth import login
import datetime
from datetime import timedelta
from auth import islogin
from auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
            return render_to_response("login_redirect.html",{})
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
            user = RegisteredUsers.objects.get(email=log_emailid)
            login(request,log_emailid,user.name)
            return HttpResponseRedirect("/search")
#            return HttpResponse("Logged In success")
        else:
            c={}
            c.update(csrf(request))
            c.update({"form":form})
            return render_to_response('index.html',c)
    if(islogin(request)):
        return HttpResponseRedirect("/search")
        
    c = {} 
    c.update(csrf(request))
    return render_to_response('index.html',c)

def search(request):
    
    if islogin(request):
        city = request.GET.get("srch_city")
        bloodgroup = request.GET.get("srch_bloodgroup")
        page = request.GET.get("page")
        if page == None:
            page = 1
        page = int(page)
        if city != None and bloodgroup != None:
            today = datetime.date.today()
            three_months = timedelta(days=90)
            results = RegisteredUsers.objects.filter(city=city,bloodgroup=bloodgroup).exclude(dolbd__gt=(today-three_months))
            paginator = Paginator(results, 10)
            name = request.session.get("name",None)
            c={}
            c.update({"user":name})
            c.update({"city":city,"bloodgroup":bloodgroup})
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                results = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                results = paginator.page(paginator.num_pages)
            c.update({"results":results})    
            return render_to_response("search.html",c)
            
        name = request.session.get("name",None)
        c={}
        c.update({"user":name})
        return render_to_response('search.html',c)
    else:
        return HttpResponseRedirect("/home")
def logoutsite(request):
    logout(request)
    return HttpResponseRedirect('/home')
def profile(request):
    if(islogin(request)):
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = RegisteredUsers.objects.get(email=request.session.get("email",None))
                try:
                    user.email = form.cleaned_data["prof_emailid"]
                    user.name = form.cleaned_data["prof_name"]
                    user.dolbd = form.cleaned_data["prof_dolbd"]
                    user.mobile = form.cleaned_data["prof_mobile"]
                    user.city = form.cleaned_data["prof_city"]
                    user.save()
                except:
                    return HttpResponse("Error in Connection with Database , Try again "+str(vars(user)))
                c={}
                c.update(csrf(request))
                email = request.session.get('email',None)
                c.update({"oldemail":email})
                c.update({"userprof":user,"updated":True})
                return render_to_response('profile.html',c)
            else:
                c={}
                email = request.session.get('email',None)
                c.update({"oldemail":email})
                c.update(csrf(request))
                c.update({"userprof":form})
                return render_to_response('profile.html',c)
        c={}
        c.update(csrf(request))
        email = request.session.get('email',None)
        userprof = RegisteredUsers.objects.get(email=email)
        #userprof = userprof[0]
        #return HttpResponse(str(vars(userprof)))
        c.update({"oldemail":email})
        c.update({"userprof":userprof})
        return render_to_response('profile.html',c)
#        return render_to_response('profile.html',c)
    else:
        return HttpResponseRedirect("/home")