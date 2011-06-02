from django.core.management.base import BaseCommand, CommandError
from pytz import timezone
from transparencycamp.uncon.models import Summize, Twitterer, Tweet
from urllib2 import urlopen
from urllib import urlencode
import datetime
import httplib
import json
import re
import rfc822

SEARCH_ENDPOINT = "/search.json"
USER_TIMELINE_RE = re.compile(r"^from:(\w+)$", re.I)
USER_TIMELINE_URL = "https://api.twitter.com/1/statuses/user_timeline.json"

def parse_datetime(s):
    dt = datetime.datetime(*rfc822.parsedate(s)[:-2], tzinfo=timezone('UTC'))
    dt = dt.astimezone(timezone('US/Eastern'))
    dt = dt.replace(tzinfo=None)
    return dt

class Command(BaseCommand):
    help = "load summize search results"
    
    def handle(self, *args, **options):
    
        conn = httplib.HTTPConnection("search.twitter.com")
    
        for summize in Summize.objects.all():
            
            match = USER_TIMELINE_RE.match(summize.value)
            
            if match:
                
                # search using the user timeline since it returns more results
                
                qs = urlencode({
                    'screen_name': match.groups()[0],
                    'count': 100,
                })
                
                url = u"%s?%s" % (USER_TIMELINE_URL, qs)
                
                res = urlopen(url)
                content = res.read()
                res.close()
                
                tweets = json.loads(content)
                
            else:
                
                # use regular old search for more advanced queries
        
                qs = urlencode({
                    'q': summize.value,
                    'since_id': summize.max_id(),
                    'rpp': 100,
                })
                path = u"%s?%s" % (SEARCH_ENDPOINT, qs)
        
                conn.request("GET", path)
                resp = conn.getresponse()
                r = json.load(resp)
                
                tweets = r['results']
            
            print len(tweets), "results for", summize.value
        
            for tweet in reversed(tweets):
                
                # update or create user
                
                if 'user' in tweet:
                    user_id = tweet['user']['id_str']
                    screen_name = tweet['user']['screen_name']
                    avatar_url = tweet['user']['profile_image_url']
                else:
                    user_id = tweet['from_user_id_str']
                    screen_name = tweet['from_user']
                    avatar_url = tweet['profile_image_url']
                
                try:
                    user = Twitterer.objects.get(twitter_id=user_id)
                    user.screen_name = screen_name
                    user.avatar_url = avatar_url
                    user.save()
                except Twitterer.DoesNotExist:
                    user = Twitterer.objects.create(
                        twitter_id=user_id,
                        screen_name=screen_name,
                        avatar_url=avatar_url,
                    )
                
                # save tweet
                
                twitter_id = tweet['id_str']
                
                try:
                    t = Tweet.objects.get(twitter_id=twitter_id)
                except Tweet.DoesNotExist:
                    t = Tweet.objects.create(
                        user=user,
                        summize=summize,
                        twitter_id=twitter_id,
                        content=tweet['text'],
                        timestamp=parse_datetime(tweet['created_at']),
                    )
    
        conn.close()