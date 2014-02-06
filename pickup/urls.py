from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pickup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pickupApp.views.index', name='index'),
    url(r'^about/', 'pickupApp.views.about', name='about'),
    url(r'^register/', 'pickupApp.views.register', name='register'),
    url(r'^home/', 'pickupApp.views.home', name='home'),
    url(r'^login/', 'pickupApp.views.user_login', name='user_login'),
    url(r'^create_game/', 'pickupApp.views.create_game', name='create_game'), 
    url(r'^logout/', 'pickupApp.views.logout_view', name='logout'),
    url(r'^user_login/', 'pickupApp.views.user_login', name='user_login'),    
    url(r'^team/', 'pickupApp.views.team', name='team'), 
    url(r'^get_games/', 'pickupApp.views.get_games', name='get_games'),
    url(r'^game/(\d+)$', 'pickupApp.views.game'), 
    url(r'^join_quit_game/', 'pickupApp.views.join_quit_game', name='join_quit_game'),

)
