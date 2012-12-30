def login(request,email):
    request.session["login"] = True
    request.session["email"] = email
    request.session.set_expiry(3600)
def logout(request):
    try:
        del request.session["login"]
        del request.session["email"]
    except:
        pass
def islogin(request):
    return request.session.get("login",False)       