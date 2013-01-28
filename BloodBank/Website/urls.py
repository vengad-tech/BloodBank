from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BloodBank.views.home', name='home'),
    # url(r'^BloodBank/', include('BloodBank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'register','Website.views.register'),
    url(r'logoutsite','Website.views.logoutsite'),
    url(r'home','Website.views.home'),
#    url(r'','Website.views.home'),
    url(r'search','Website.views.search'),
    url(r'profile','Website.views.profile'),    
    url(r'changepswd','Website.views.changepswd'),    
    url(r'forgotpswd','Website.views.forgotpswd'),    
    url(r'terms','Website.views.terms'),    
    url(r'siteby','Website.views.siteby'),    
    url(r'contact','Website.views.contact'),    
    url(r'reportuser','Website.views.reportinactivity'),
    url(r'healthtips','Website.views.healthtips')

)
