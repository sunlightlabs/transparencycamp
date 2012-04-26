from dateutil.parser import parse as parsedate
from django.utils.html import urlize
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from transparencycamp.uncon.models import Conference, Session, Summize, Tweet, Twitterer, FlickrPhoto
import datetime


class CurrentConferenceResource(ModelResource):
    class Meta:
        queryset = Conference.objects.current()
        resource_name = "current_conference"


class ConferenceResource(ModelResource):
    class Meta:
        queryset = Conference.objects.all()
        resource_name = "conferences"


class SessionResource(ModelResource):
    class Meta:
        excludes = ('has_wiki', )
        filtering = {
            'slug': ('exact', ),
            'location': ('exact', ),
            'date': ('exact', 'gt', 'gte', 'lt', 'lte'),
            'start_time': ('exact', 'gt', 'gte', 'lt', 'lte'),
            'end_time': ('exact', 'gt', 'gte', 'lt', 'lte'),
        }
        queryset = Conference.objects.current_conference().sessions.all()
        resource_name = "sessions"

    def serialize(self, request, data, format, options=None):
        resp = super(SessionResource, self).serialize(request, data, format, options)
        return resp

    def dehydrate(self, x):
        x.data['url'] = "http://transparencycamp.org/sessions/%s/" % x.data['id']
        return x

    def build_filters(self, filters=None):

        if filters is None:
            filters = {}

        orm_filters = super(SessionResource, self).build_filters(filters)

        now = datetime.datetime.now() - datetime.timedelta(0, 60 * 15)
        con = Conference.objects.current_conference()

        if "today" in filters:
            orm_filters['date'] = now.date()
        elif "latertoday" in filters:
            orm_filters['date'] = now.date()
            orm_filters['start_time__gte'] = now.time()
        elif "tomorrow" in filters:
            orm_filters['date'] = now.date() + datetime.timedelta(1)
        elif "next" in filters:
            next_timeslot = con.next_timeslot(now.date(), now.time())
            orm_filters['date'] = now.date()
            orm_filters['start_time'] = next_timeslot

        return orm_filters


class PhotoResource(ModelResource):
    class Meta:
        excludes = ('id',)
        queryset = FlickrPhoto.objects.all()
        resource_name = "photos"

    def dehydrate(self, x):

        url_format = "http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s_%(size)s.jpg"

        params = {
            'farm': x.data['farm'],
            'server': x.data['server'],
            'id': x.data['flickr_id'],
            'secret': x.data['secret'],
            'owner': x.data['owner'],
        }

        params['size'] = 's'
        x.data['url_square'] = url_format % params

        params['size'] = 't'
        x.data['url_thumbnail'] = url_format % params

        params['size'] = 'm'
        x.data['url_small'] = url_format % params

        params['size'] = '-'
        x.data['url_medium500'] = url_format % params

        params['size'] = 'z'
        x.data['url_medium640'] = url_format % params

        params['size'] = 'b'
        x.data['url_large'] = url_format % params

        params['size'] = 'o'
        x.data['url_original'] = url_format % params

        x.data['url'] = "http://www.flickr.com/photos/%(owner)s/%(id)s" % params

        return x


class TwittererResource(ModelResource):
    class Meta:
        excludes = ('id', 'full_name', 'twitter_id')
        include_resource_uri = False
        queryset = Twitterer.objects.all()


class AbstractTweetResource(ModelResource):
    user = fields.ToOneField(TwittererResource, 'user', full=True)

    def dehydrate(self, x):
        url = "http://twitter.com/%s/status/%s"
        x.data['content'] = urlize(x.data['content'])
        x.data['pubdate'] = x.data['timestamp'].strftime("%I:%M%p, %B %d, %Y")
        x.data['url'] = url % (x.data['user'].data['screen_name'], x.data['twitter_id'])
        return x


class UpdatesResource(AbstractTweetResource):
    class Meta:
        filtering = {
            'timestamp': ('exact', 'gt', 'gte', 'lt', 'lte'),
            'twitter_id': ('exact', ),
        }
        queryset = Tweet.objects.filter(user__screen_name="TCampDC")


class SocialFeedResource(AbstractTweetResource):
    class Meta:
        filtering = {
            'timestamp': ('exact', 'gt', 'gte', 'lt', 'lte'),
            'twitter_id': ('exact',),
        }
        queryset = Tweet.objects.filter(summize__slug="socialfeed")
