def login(request,email,name=None):
    request.session["login"] = True
    request.session["email"] = email
    request.session["name"]=name
    request.session.set_expiry(3600)
def logout(request):
    try:
        del request.session["login"]
        del request.session["email"]
        del request.session["name"]
    except:
        pass
def islogin(request):
    return request.session.get("login",False)       