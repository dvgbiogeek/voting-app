from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from chilies.views import home, meme_display
from chilies.resources.meme_resource import MemeResource
from chilies.resources.vote_resource import VoteResource
from chilies.resources.user_resource import UserResource
from chilies.resources.score_resource import ScoreResource
from accounts.views import register


v1_api = Api(api_name='v1')
v1_api.register(MemeResource())
v1_api.register(VoteResource())
v1_api.register(UserResource())
v1_api.register(ScoreResource())


urlpatterns = patterns('',
    # Home page
    url(r'^$', 'chilies.views.home', name='home'),
    # Account urls
    url(r'^login/$', 'django.contrib.auth.views.login', {
            'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
            'template_name': 'home.html'}),
    url(r'^new_account/$', 'accounts.views.register', name='register'),
    # Random generator Json
    url(r'^chilies/test$', 'chilies.views.meme_display',
            name='meme_display'),
    # Backend apis
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
