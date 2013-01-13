import urllib2
def sendpassword(name,email,password):
    req = urllib2.Request('http://slmbldbank.appspot.com/?name='+name+'&to='+email+'&password='+password)
    response = urllib2.urlopen(req)
    the_page = response.read()