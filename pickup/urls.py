from django.conf.urls import patterns, include, url
#from django.conf.urls import *
import notifications
import actstream

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
    url(r'^delete_game/', 'pickupApp.views.delete_game', name='delete_game'),
    url(r'^sport/(\w+)$', 'pickupApp.views.sport', name='sport'),
    url(r'^user/(\d+)$', 'pickupApp.views.user', name='user'), 
    url(r'^inbox/notifications/', include(notifications.urls)),
    url(r'^activity/', include('actstream.urls')),
    url(r'^remove_notifications/', 'pickupApp.views.remove_notifications', name='remove_notifications'),
    url(r'^profile/', 'pickupApp.views.profile', name='profile'),
    url(r'^sports/', 'pickupApp.views.sports', name='sports'),   
    url(r'^search/', 'pickupApp.views.search', name='search'), 
    # url(r'', include('social_auth.urls')),
    url(r'^comment/', 'pickupApp.views.comment', name='comment'), 
    url(r'^instagram_login/', 'pickupApp.views.instagram_login', name='instagram_login'),
    url(r'^get_instagram_photos/(\d+)$', 'pickupApp.views.get_instagram_photos', name='get_instagram_photos'),
    url(r'^post_photos/', 'pickupApp.views.post_photos', name='post_photos'),
    url(r'^upload_profile_photo/', 'pickupApp.views.upload_profile_photo', name='upload_profile_photo'),
    url(r'^toggle_follow/','pickupApp.views.toggle_follow',name='toggle_follow'),
    url(r'^analytics/', 'pickupApp.views.analytics', name='analytics'),
    url(r'^first_login/', 'pickupApp.views.first_login', name='first_login'),
    url(r'^first_login2/', 'pickupApp.views.first_login2', name='first_login2'),
    url(r'^invite_friends/(\d+)$', 'pickupApp.views.invite_friends', name='invite_friends'),
    url(r'^recommendations/', 'pickupApp.views.recommendations', name='recommendations'),   
    url(r'^store_user_location/', 'pickupApp.views.store_user_location', name='store_user_location'),   
)

# urlpatterns = urlpatterns + 
#     patterns('',
#         url(r'^inbox/notifications/', include(notifications.urls)),
#     )