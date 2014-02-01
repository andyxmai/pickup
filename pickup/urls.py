from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pickup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pickupApp.views.index', name='index'),
    url(r'^register/', 'pickupApp.views.register', name='register'),
    url(r'^home/', 'pickupApp.views.home', name='home'),
    url(r'^login/', 'pickupApp.views.user_login', name='user_login'),
    url(r'^create_game/', 'pickupApp.views.create_game', name='create_game'), 
    url(r'^logout/', 'pickupApp.views.logout', name='logout'),
    url(r'^home/', 'pickupApp.views.home', name='home'), 
    url(r'^base/', 'pickupApp.views.base', name='base'), 
    url(r'^features/', 'pickupApp.views.features', name='features'),
    url(r'^game/', 'pickupApp.views.game', name='game'),   
    url(r'^user_login/', 'pickupApp.views.user_login', name='user_login'),    
    url(r'^team/', 'pickupApp.views.team', name='team'),    
)
