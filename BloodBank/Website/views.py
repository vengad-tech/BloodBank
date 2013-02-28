# Create your views here.
from django.http import HttpResponse
#from django.http import HttpResponse, HttpResponseRedirectBase
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from forms import RegisterForm
from forms import PreregisterForm
from forms import LoginForm
from forms import SearchForm
from forms import ProfileForm
from email import sendpassword
from django.core.context_processors import csrf
from models import RegisteredUsers
from django.shortcuts import render
from auth import login
import datetime
from datetime import timedelta
from auth import islogin
from auth import logout
from forms import PasswordForm
from forms import ForgotPassword
from models import Feedback
from forms import ContactForm
from BloodBank import settings 
#from recaptcha.client import captcha
from recaptcha.client.captcha import displayhtml
from recaptcha.client.captcha import submit

import sys
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.contrib.formtools.tests.wizard.forms import request
#from django.contrib.formtools.tests.wizard.forms import request

#def display_form(request):
#    form = SomeForm()
#    # assuming your keys are in settings.py
#    public_key = settings.RECAPTCHA_PUBLIC_KEY
#    script = displayhtml(public_key=public_key)
#    return render_to_response('form.html', {'form':form,'script':script}, context_instance=RequestContext(request))
#)
    
def check_captcha(request):
    remote_ip = request.META['REMOTE_ADDR']
    challenge = request.POST['recaptcha_challenge_field']
    response = request.POST['recaptcha_response_field']
    private_key = settings.RECAPTCHA_PRIVATE_KEY
    return submit(challenge, response, private_key, remote_ip)

def register(request):
    public_key = settings.RECAPTCHA_PUBLIC_KEY
    script = displayhtml(public_key=public_key)
#    form = RegisterForm(request.POST())
#    if form.reg_location != None:
#    result = check_captcha(request)
    if request.method == 'POST': # If the form has been submitted...
        form = RegisterForm(request.POST) # A form bound to the POST data
        #public_key = settings.RECAPTCHA_PUBLIC_KEY
        
#        if form.is_valid():
        hasLocation = True
        try:
            a = request.POST["reg_location"]
        except:
            hasLocation = False
            
        if hasLocation:
            result = check_captcha(request)
            if form.is_valid() and result.is_valid: # All validation rules pass
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
                    #if user.dolbd is None:
                    #    user.dolbd = "1991-01-01"
                    user.sex = form.cleaned_data["reg_sex"]
                    user.mobile = str(form.cleaned_data["reg_mobile"])
                    user.hidemob = form.cleaned_data["reg_hidemob"]
                    user.city = form.cleaned_data["reg_city"]
                    user.location = form.cleaned_data["reg_location"]
                    user.save()
                except:
                    print sys.exc_info()[1]
                    return HttpResponse("Error in Connection with Database , Try again "+str(vars(user)))
                return render_to_response("login_redirect.html",{})
                #return HttpResponseRedirect('/registered/') # Redirect after POST
            else:
                
                c={}
                c.update(csrf(request))
                if(result.is_valid != True):
                    c.update({"captchaerror":True})
                c.update({'script':script})
                c.update({"form":form})
                c.update({"test":"testing"})
                c.update({"reg":True})
                #r-turn HttpResponse("validation failed because "+str(c))
                return render_to_response('index.html',c)
        else:
            c = {}
            c.update({"form":form})
            c.update({"reg":True})
            c.update(csrf(request))
            c.update({'script':script})
            return render_to_response('index.html',c)
    c = {}
    c.update({"reg":True})
    c.update(csrf(request))
    c.update({'script':script})
    return render_to_response('index.html',c)

def preregister(request):
#    public_key = settings.RECAPTCHA_PUBLIC_KEY
#   script = displayhtml(public_key=public_key)
    if request.method == 'POST':
        form = PreregisterForm(request.POST)
#        result = check_captcha(request)
#        if form.is_valid() and result.is_valid:
        if form.is_valid:
            c={}
#            c.update({'script':script})
            c.update(csrf(request))
            c.update({"form":form})
            c.update({"reg":True})
            return render_to_response('index.html',c)
        else:
            c={}
            c.update(csrf(request))
            c.update({"form":form})
            c.update({"prereg":True})
            return render_to_response('index.html',c)
    c={}
    c.update(csrf(request))
    c.update({"prereg":True})
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
    load_location = "no"
    try:
        load_location = request.GET["load_location"]
    except:
        load_location = "no"
        
    if islogin(request):
#       
        city = request.GET.get("srch_city")
        bloodgroup = request.GET.get("srch_bloodgroup")
        location = request.GET.get("reg_location")
    #        age = None
        age = datetime.date.today()
        page = request.GET.get("page")
        if page == None:
            page = 1
        page = int(page)
        if city != None and bloodgroup != None and location !=None:
            today = datetime.date.today()
            three_months = timedelta(days=90)
            eighteen_years = timedelta(days=6570)
            results = RegisteredUsers.objects.filter(city=city,bloodgroup=bloodgroup,location=location).exclude(dolbd__gt=(today-three_months)).exclude(dob__gt=(today-eighteen_years))
    #            results = RegisteredUsers.objects.get(city=city,bloodgroup=bloodgroup).exclude(dolbd__gt=(today-three_months))
    #            age = today - age
    #            age = today - results.dob
            for res in results:
                dt = today  - res.dob
                res.age = dt.days / 365 
            paginator = Paginator(results, 5)
            name = request.session.get("name",None)
            c={}
            c.update({"user":name})
            c.update({"city":city,"bloodgroup":bloodgroup,"location":location})
            c.update({"age":age})
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
        c.update({"city":city,"bloodgroup":bloodgroup})
        return render_to_response('search.html',c)
    else:
        return HttpResponseRedirect("/")

def logoff(request):
    logout(request)
    return HttpResponseRedirect('/')

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
                    user.mobile = str(form.cleaned_data["prof_mobile"])
                    user.city = form.cleaned_data["prof_city"]
#                    user.location = form.cleaned_data["reg_location"]
                    user.save()
                except:
                    return HttpResponse("Error in Connection with Database , Please Try again "+str(vars(user)))
                c={}
                c.update(csrf(request))
                email = request.session.get('email',None)
                name = request.session.get('name',None)
                c.update({"oldemail":email,"user":name})
                c.update({"userprof":user,"updated":True})
                return render_to_response('profile.html',c)
            else:
                c={}
                email = request.session.get('email',None)
                name = request.session.get('name',None)
                c.update({"oldemail":email,"user":name})
                c.update(csrf(request))
                c.update({"userprof":form})
                return render_to_response('profile.html',c)
        c={}
        c.update(csrf(request))
        email = request.session.get('email',None)
        name = request.session.get('name',None)
        userprof = RegisteredUsers.objects.get(email=email)
#        location = userprof.location
        #userprof = userprof[0]
        #return HttpResponse(str(vars(userprof)))
        c.update({"oldemail":email,"user":name})
        c.update({"userprof":userprof})
#        c.update({"location":location})
        return render_to_response('profile.html',c)
#        return render_to_response('profile.html',c)
    else:
        return HttpResponseRedirect("/")
    
def changepswd(request):
    if(islogin(request)==False):
        return HttpResponseRedirect("/")
    emailid = request.session.get("email",None)
    name = request.session.get("name",None)
    if request.method =="POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            try:
                user = RegisteredUsers.objects.get(email=emailid)
                user.pswd = form.cleaned_data["new_pswd"]
                user.save()
                c= {}
                c.update(csrf(request))
                c.update({"emailid":emailid,"user":name})
                c.update({"updated":True})
                return render_to_response("changepswd.html",c)
            except:
                return HttpResponse("Error in Connection with Database , Try again ")
        else:
            c={}
            c.update(csrf(request))
            c.update({"passwordform":form})
            c.update({"emailid":emailid,"user":name})
            #return HttpResponse(str(vars(form)))
            return render_to_response("changepswd.html",c)    
    c={}
    c.update(csrf(request))
    
    c.update({"emailid":emailid})
    return render_to_response("changepswd.html",c)

def forgotpswd(request):
    if request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid():
            try:
                emailid = form.cleaned_data["frgt_email"]
                user = RegisteredUsers.objects.get(email=emailid)
                if user != None :
                    name=user.name
                    password = user.pswd
                    email = user.email
                    #write coding to send email to the mail
                    sendpassword(name,email,password)
                    c={}
                    c.update({"success":True})
                    c.update(csrf(request))
                else:
                    c={}
                    c.update(csrf(request))
                    c.update({"error":True})
                return render_to_response("forgotpswd.html",c)
            except:
                c={}
                c.update(csrf(request))
                c.update({"error":True})
                return render_to_response("forgotpswd.html",c)
        else:
            c={}
            c.update(csrf(request))
            c.update({"form":form})    
            return render_to_response('forgotpswd.html',c)
    c={}
    c.update(csrf(request))
    return render_to_response('forgotpswd.html',c)

def contact(request):
    if request.method == 'POST':
        c={}
        form = ContactForm(request.POST)
        if form.is_valid():
            feedback = Feedback()
            try:
                feedback.name = form.cleaned_data["con_name"]
                feedback.email = form.cleaned_data["con_emailid"]
                try:
                    feedback.mobile = str(form.cleaned_data["con_mobile"])
                except:
                    feedback.mobile = ""
                #if feedback.mobile is None:
                #    feedback.mobile = 0
                feedback.value = form.cleaned_data["con_text"]
                feedback.save()
                c.update({"success":True})
            except:
                print sys.exc_info()[1]
                return HttpResponse('Error in sending feedback'+str(vars(feedback))+str(sys.exc_info()[0]))
            
            c.update(csrf(request))
            return render_to_response('contact.html',c)
        else:
            c={}
            c.update({"form":form})
            c.update(csrf(request))
            return render_to_response('contact.html',c)
    c={}
    c.update(csrf(request))
    return render_to_response('contact.html',c)

def terms(request):
    return render_to_response("terms.html")

def site(request):
    return render_to_response('site.html')

def reportinactivity(request):
    return render_to_response('reportuser_redirect.html')

def healthtips(request):
    return render_to_response('healthtips.html')
