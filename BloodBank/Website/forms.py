from django import forms
import datetime
from datetime import timedelta
import re
from models import RegisteredUsers
class RegisterForm(forms.Form):
    reg_name=forms.CharField(30,3)
    reg_emailid = forms.EmailField()
    reg_pswd = forms.CharField(None,5)
    reg_cnfpswd= forms.CharField(None,5)
    reg_bloodgroup = forms.CharField(4,2)
    reg_mobile = forms.IntegerField()
    reg_hidemob = forms.CharField(required=False)
    reg_sex = forms.CharField(6,4)
    reg_dob = forms.DateField()
    reg_dolbd = forms.DateField()
    reg_city = forms.CharField(20,3)
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
            if reg_dob > today - year :
                msg = u"Must be 18 years or Older "
                self._errors["reg_dob"] = self.error_class([msg])
        except:
            pass
        try:
            if  reg_dolbd > today :
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
            if re.match(r'^[a-zA-Z.]*$', reg_name) is None:
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
    
        