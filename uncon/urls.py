from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from transparencycamp.uncon.resources import (
    CurrentConferenceResource, ConferenceResource, SessionResource,
    UpdatesResource, SocialFeedResource, PhotoResource)

api = Api(api_name='api')
api.register(CurrentConferenceResource())
api.register(ConferenceResource())
api.register(SessionResource())
api.register(UpdatesResource())
api.register(SocialFeedResource())
api.register(PhotoResource())

urlpatterns = patterns('',
    url(r'^sessions/$', 'transparencycamp.uncon.views.session_list'),
    url(r'^sessions/(?P<pk>\d+)/$', 'transparencycamp.uncon.views.session_detail', name='session_detail'),
    url(r'^sessions/(?P<con_slug>[\w\-]+)/$', 'transparencycamp.uncon.views.session_list'),
    url(r'^', include(api.urls)),
)