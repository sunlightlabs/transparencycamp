from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from transparencycamp.uncon.models import FlickrPhoto
from urllib2 import urlopen
from urllib import urlencode
import json

API_KEY = getattr(settings, 'UNCON_FLICKR_API_KEY', None)
TAGS = getattr(settings, 'UNCON_FLICKR_TAGS', None)

ENDPOINT = "http://api.flickr.com/services/rest/"

class Command(BaseCommand):
    help = "load photos from Flickr based on tags"
    
    def handle(self, *args, **options):
        
        params = {
            'api_key': API_KEY,
            'method': 'flickr.photos.search',
            'format': 'json',
            'nojsoncallback': 1,
        }
        
        if TAGS:
            params['tags'] = TAGS
    
        qs = urlencode(params)
        
        res = urlopen("%s?%s" % (ENDPOINT, qs))
        content = res.read()
        res.close()
        
        response = json.loads(content)
        
        for remote_photo in response['photos']['photo']:
            
            try:
                FlickrPhoto.objects.get(flickr_id=remote_photo['id'])
            except FlickrPhoto.DoesNotExist:
                FlickrPhoto.objects.create(
                    flickr_id=remote_photo['id'],
                    owner=remote_photo['owner'],
                    secret=remote_photo['secret'],
                    server=remote_photo['server'],
                    farm=remote_photo['farm'],
                    title=remote_photo['title'],
                )
        