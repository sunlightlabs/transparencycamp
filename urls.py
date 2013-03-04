from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to
import os

admin.autodiscover()

# generic views
urlpatterns = patterns('django.views.generic.simple',
    url(r'^community/$', "direct_to_template", {'template': 'community.html'}),
    url(r'^donate/$', "direct_to_template", {'template': 'donate.html'}),
    url(r'^viphackathon/$', "direct_to_template", {'template': 'hackathon.html'}),
    url(r'^logistics/$', "direct_to_template", {'template': 'logistics.html'}),
    url(r'^schedule/$', "redirect_to", {'url': '/sessions/'}),
    url(r'^sponsors/$', "direct_to_template", {'template': 'sponsors.html'}),
    url(r'^sponsors/info/$', "direct_to_template", {'template': 'sponsors_info.html'}),
    url(r'^staff/$', "redirect_to", {'url': '/staff/login/'}),
    url(r'^survey/$', "redirect_to", {'url': 'http://local.publicequalsonline.com/page/signup/TransparencyCamp_Survey'}),
    url(r'^how-to/$', "direct_to_template", {'template': 'howto.html'}),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/', include('googleauth.urls')),
    url(r'^login/$', "transparencycamp.tc.views.login", name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', 'redirect_field_name': 'next'}, name='logout'),
    url(r'^logged-in/$', 'transparencycamp.tc.views.logged_in', name='logged_in'),
    url(r'^live/$', 'transparencycamp.tc.views.live'),
    url(r'^wiki/$', redirect_to, {'url': '/'}),
    url(r'^wiki/2011/dc/(?P<day>\w+)/(?P<title>[\w\-]+)/$', "transparencycamp.uncon.views.wiki_redirect"),
    url(r'^wiki/', include('markupwiki.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^', include('transparencycamp.uncon.urls')),
    url(r'^', include('brainstorm.urls')),
    url(r'^$', 'transparencycamp.tc.views.index', name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^bigscreen/$', 'django.views.generic.simple.redirect_to', {'url': '/bigscreen/index.html'}),
        url(r'^bigscreen/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': os.path.join(settings.PROJECT_ROOT, 'www', 'bigscreen'),
        }),
        url(r'^mobile/$', 'django.views.generic.simple.redirect_to', {'url': '/mobile/index.html'}),
        url(r'^mobile/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': os.path.join(settings.PROJECT_ROOT, 'www', 'mobile'),
        }),
    )
