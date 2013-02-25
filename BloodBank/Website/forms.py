from django import forms
from BloodBank import settings
import datetime
from datetime import timedelta
import re
from models import RegisteredUsers
from models import Feedback
#from recaptcha.client import captcha

class ContactForm(forms.Form):
    con_name=forms.CharField(30,3)
    con_emailid=forms.EmailField(required=False)
    #con_mobile = forms.CharField(required=False)
    con_mobile=forms.IntegerField(required=False)
    con_text=forms.CharField(300,3)
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        con_name=cleaned_data.get("con_name")
        con_emailid=cleaned_data.get("con_emailid")
        con_mobile=cleaned_data.get("con_mobile")
        con_text=cleaned_data.get("con_text")
        try:
            if re.match(r'^[A-Za-z. ]*$', con_name) is None:
                msg = u"Invalid Characters in Name"
                self._errors["con_name"] = self.error_class([msg])
        except:
            pass
        try:
            if con_mobile != None and (con_mobile < 7000000000 or con_mobile > 9999999999):
                msg = u"Invalid Mobile Number"
                self._errors["con_mobile"] = self.error_class([msg])
        except:
            pass
        
        return cleaned_data
    
class ProfileForm(forms.Form):
    prof_oldemail=forms.EmailField()
    prof_name = forms.CharField(30,3)
    prof_emailid = forms.EmailField()
    prof_mobile = forms.IntegerField()
    prof_dolbd = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    prof_city = forms.CharField(20,3)
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        prof_emailid = cleaned_data.get("prof_emailid")
        prof_oldemail = cleaned_data.get("prof_oldemail")
        prof_dob = cleaned_data.get("prof_dob")
        
        prof_dolbd = cleaned_data.get("prof_dolbd")
        today = datetime.date.today()
        prof_mobile = cleaned_data.get("prof_mobile")
        prof_name = cleaned_data.get("prof_name")
        #18 yrs minimum to donate blood
        year = timedelta(days=365*18)
        try:
            if prof_dob > today :
                msg = u"Must be 1 day or Older "
                self._errors["prof_dob"] = self.error_class([msg])
        except:
            pass
        try:
            if  prof_dolbd !=None and prof_dolbd > today :
                msg = u"Enter a Resonable Date "
                self._errors["prof_dolbd"] = self.error_class([msg])
            else:
                self._errors["prof_dolbd"]
        except:
            pass
        try:
            if prof_mobile < 7000000000 or prof_mobile > 9999999999:
                msg = u"Invalid Mobile number "
                self._errors["prof_mobile"] = self.error_class([msg])
        except:
            pass
        try:
            if re.match(r'^[A-Za-z. ]*$', prof_name) is None:
                msg = u"Invalid Characters in Name "
                self._errors["prof_name"] = self.error_class([msg])
        except:
            pass
                
        #checking if email id is already registerd or not 
        try:
            if prof_emailid != prof_oldemail :
                user = RegisteredUsers.objects.filter(email=prof_emailid)
                if len(user) > 0 :
                    msg = u"Email ID already registerd "
                    self._errors["prof_emailid"] = self.error_class([msg])
        except:        
            pass
            
         
        
        
        

        # Always return the full collection of cleaned data.
        return cleaned_data

class PreregisterForm(forms.Form):
    pre_reg_name=forms.CharField(30,3)
    pre_reg_emailid = forms.EmailField()
    pre_reg_pswd = forms.CharField(None,5)
    pre_reg_cnfpswd= forms.CharField(None,5)
    pre_reg_bloodgroup = forms.CharField(4,2)
    pre_reg_mobile = forms.IntegerField()
    pre_reg_hidemob = forms.CharField(required=False)
    pre_reg_sex = forms.CharField(6,4)
    pre_reg_dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    pre_reg_dolbd = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    pre_reg_city = forms.CharField(20,3)
    def clean(self):
        cleaned_data = super(PreregisterForm, self).clean()
        pre_reg_emailid = cleaned_data.get("pre_reg_emailid")
        pre_reg_pswd = cleaned_data.get("pre_reg_pswd")
        pre_reg_cnfpswd = cleaned_data.get("pre_reg_cnfpswd")
        pre_reg_dob = cleaned_data.get("pre_reg_dob")
        pre_reg_dolbd = cleaned_data.get("pre_reg_dolbd")
        today = datetime.date.today()
        pre_reg_mobile = cleaned_data.get("pre_reg_mobile")
        pre_reg_name = cleaned_data.get("pre_reg_name")
        #18 yrs minimum to donate blood
        year = timedelta(days=365*18)
        try:
            if pre_reg_dob > today :
                msg = u"Must be 1 day or Older "
                self._errors["pre_reg_dob"] = self.error_class([msg])
        except:
            pass
        try:
            if  pre_reg_dolbd != None and (pre_reg_dolbd > today or pre_reg_dolbd < pre_reg_dob + year):
                msg = u"Enter a Resonable Date "
                self._errors["pre_reg_dolbd"] = self.error_class([msg])
        except:
            pass
        try:
            if pre_reg_mobile < 7000000000 or pre_reg_mobile > 9999999999:
                msg = u"Invalid Mobile number "
                self._errors["pre_reg_mobile"] = self.error_class([msg])
        except:
            pass
        try:
            if re.match(r'^[a-zA-Z. ]*$', pre_reg_name) is None:
                msg = u"Invalid Characters in Name "
                self._errors["pre_reg_name"] = self.error_class([msg])
        except:
            pass
                
        #checking if email id is already registerd or not 
        try:
            user = RegisteredUsers.objects.filter(email=pre_reg_emailid)
            if len(user) > 0 :
                msg = u"Email ID already registerd "
                self._errors["pre_reg_emailid"] = self.error_class([msg])
        except:        
            pass
        if pre_reg_pswd != pre_reg_cnfpswd:
            # We know these are not in self._errors now (see discussion
            # below).
            msg = u"Password Doesnt match"
            self._errors["pre_reg_pswd"] = self.error_class([msg])
            self._errors["pre_reg_cnfpswd"] = self.error_class([msg])

            # These fields are no longer valid. Remove them from the
            # cleaned data.
            try:
                del cleaned_data["pre_reg_pswd"]
                del cleaned_data["pre_reg_cnfpswd"]
            except:
                pass

        # Always return the full collection of cleaned data.
        return cleaned_data
    
        
        
class RegisterForm(forms.Form):
    reg_name=forms.CharField(30,3)
    reg_emailid = forms.EmailField()
    reg_pswd = forms.CharField(None,5)
    reg_cnfpswd= forms.CharField(None,5)
    reg_bloodgroup = forms.CharField(4,2)
    reg_mobile = forms.IntegerField()
    reg_hidemob = forms.CharField(required=False)
    reg_sex = forms.CharField(6,4)
    reg_dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    reg_dolbd = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    reg_city = forms.CharField(20,3)
    reg_location = forms.CharField(30,3)
    
    def clean(self):
        
        cleaned_data = super(RegisterForm, self).clean()
        reg_emailid = cleaned_data.get("reg_emailid")
        pswd = cleaned_data.get("reg_pswd")
        cnfpswd = cleaned_data.get("reg_cnfpswd")
        reg_dob = cleaned_data.get("reg_dob")
        reg_dolbd = cleaned_data.get("reg_dolbd")
        today = datetime.date.today()
        reg_mobile = cleaned_data.get("reg_mobile")
        reg_name = cleaned_data.get("reg_name")
        #18 yrs minimum to donate blood
        year = timedelta(days=365*18)
        try:
            if reg_dob > today :
                msg = u"Must be 1 day or Older "
                self._errors["reg_dob"] = self.error_class([msg])
        except:
            pass
        try:
            if  reg_dolbd != None and (reg_dolbd > today or reg_dolbd < reg_dob + year):
                msg = u"Enter a Resonable Date "
                self._errors["reg_dolbd"] = self.error_class([msg])
        except:
            pass
        try:
            if reg_mobile < 7000000000 or reg_mobile > 9999999999:
                msg = u"Invalid Mobile number "
                self._errors["reg_mobile"] = self.error_class([msg])
        except:
            pass
        try:
            if re.match(r'^[a-zA-Z. ]*$', reg_name) is None:
                msg = u"Invalid Characters in Name "
                self._errors["reg_name"] = self.error_class([msg])
        except:
            pass
                
        #checking if email id is already registerd or not 
        try:
            user = RegisteredUsers.objects.filter(email=reg_emailid)
            if len(user) > 0 :
                msg = u"Email ID already registerd "
                self._errors["reg_emailid"] = self.error_class([msg])
        except:        
            pass
            
         
        
        
        if pswd != cnfpswd:
            # We know these are not in self._errors now (see discussion
            # below).
            msg = u"Password Doesnt match"
            self._errors["reg_pswd"] = self.error_class([msg])
            self._errors["reg_cnfpswd"] = self.error_class([msg])

            # These fields are no longer valid. Remove them from the
            # cleaned data.
            try:
                del cleaned_data["reg_pswd"]
                del cleaned_data["reg_cnfpswd"]
            except:
                pass

        # Always return the full collection of cleaned data.
        return cleaned_data
    
    
class LoginForm(forms.Form):
    log_emailid= forms.EmailField()
    log_pswd = forms.CharField(30,5)
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        
        try:
            log_emailid = cleaned_data["log_emailid"]
            log_pswd = cleaned_data["log_pswd"]
            user =RegisteredUsers.objects.get(email=log_emailid,pswd=log_pswd)
        except:
            msg =u"Invalid User Name or Password "
            self._errors["log_pswd"] = self.error_class([msg])
        return cleaned_data
class SearchForm(forms.Form):
    srch_bloodgroup = forms.CharField(6,3)
    srch_city = forms.CharField(20,3)
    
class PasswordForm(forms.Form):
    emailid = forms.EmailField()
    old_pswd=forms.CharField(30,5)
    new_pswd=forms.CharField(30,5)
    cnf_new_pswd = forms.CharField(30,5)
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        emailid=cleaned_data["emailid"]
        old_pswd = ""
        try:
            old_pswd = cleaned_data["old_pswd"]
        except:
            old_pswd = None
            msg =u"Invalid Password "
            self._errors["old_pswd"] = self.error_class([msg])
            return cleaned_data
        new_pswd = ""
        cnf_new_pswd =""
        try:
            new_pswd = cleaned_data["new_pswd"]
            cnf_new_pswd = cleaned_data["cnf_new_pswd"]
        except:
            msg =u"Invalid Password or Empty"
            self._errors["cnf_new_pswd"] = self.error_class([msg])
            #self._errors["cnf_new_pswd"] = "Invalid Password or Empty"
            return cleaned_data
        try:
            users = RegisteredUsers.objects.filter(email=emailid,pswd=old_pswd)
            if len(users) == 0:
                msg =u"Wrong Password"
                self._errors["old_pswd"] = self.error_class([msg])
            if new_pswd != cnf_new_pswd :
                msg =u"Passwords do not match"
                self._errors["cnf_new_pswd"] = self.error_class([msg])
        except:
            msg =u"Unknown Error occured,Try after some time"
            self._errors["cnf_new_pswd"] = self.error_class([msg])
        return cleaned_data
class ForgotPassword(forms.Form):
    frgt_email = forms.EmailField()
            