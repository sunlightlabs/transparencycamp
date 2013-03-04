from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from brainstorm.models import Idea
from brainstorm.feeds import SubsiteFeed

# feeds live at rss/latest/site-name/
urlpatterns = patterns('',
    url(r'^rss/latest/$', SubsiteFeed()),
)

urlpatterns += patterns('brainstorm.views',
    url(r'^(?P<slug>[\w-]+)/$', 'idea_list', {'ordering': 'most_popular'}, name='ideas_popular'),
    url(r'^(?P<slug>[\w-]+)/latest/$', 'idea_list', {'ordering': 'latest'}, name='ideas_latest'),
    url(r'^(?P<slug>[\w-]+)/(?P<id>\d+)/$', 'idea_detail', name='idea_detail'),
    url(r'^(?P<slug>[\w-]+)/new_idea/$', 'new_idea', name='new_idea'),
    url(r'^(?P<slug>[\w-]+)/(?P<id>\d+)/votes(?P<format>(\.json))?/?$',
        'vote', name='idea_vote'),
    # url(r'^vote(?P<format>(\.json))?/?$', 'vote', name='idea_vote'),
)
