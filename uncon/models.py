from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Min
from django.template.loader import render_to_string
from markupwiki.models import Article, ArticleVersion
import datetime

#
# conference and session models
#

class ConferenceManager(models.Manager):
    def current_conference(self):
        cid = getattr(settings, 'CURRENT_CONFERENCE_ID', None)
        if cid is not None:
            try:
                return Conference.objects.get(pk=int(cid))
            except ValueError:
                pass # int conversion failed, fall through and return None

class Conference(models.Model):
    objects = ConferenceManager()
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    class Meta:
        ordering = ('start_date',)
    
    def __unicode__(self):
        return self.name
    
    def next_timeslot(self, date=None, time=None):
        
        if not date:
            date = datetime.date.today()
        if not time:
            now = datetime.datetime.now() - datetime.timedelta(0, 60 * 15)
            time = now.time()
        
        res = self.sessions.filter(date=date, start_time__gt=time).aggregate(Min('start_time'))
        
        return res['start_time__min']
    
    def next_sessions(self):
        today = datetime.datetime.now()
        next_timeslot = self.next_timeslot()
        return self.sessions.filter(date=today.date(), start_time=next_timeslot)
        

class Session(models.Model):
    conference = models.ForeignKey(Conference, related_name="sessions")
    article = models.ForeignKey(Article, related_name="session", unique=True, blank=True, null=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    organized_by = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=64)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(User, related_name="created_sessions")
    has_wiki = models.BooleanField(default=True)

    class Meta:
        unique_together = ('conference','slug')
        ordering = ('date','start_time','slug',)
    
    def __unicode__(self):
        return self.title
    
    def save(self, **kwargs):
        
        title = "%s/%s/%s" % (self.conference.slug.replace('-', '/'),
                              self.date.strftime("%A").lower(),
                              self.title.replace(' ', '_').lower())
        
        if not self.article:
                               
            self.article = Article.objects.create(
                title=title,
                creator=self.created_by,
            )
            
            ArticleVersion.objects.create(
                article=self.article,
                author=self.created_by,
                number=0,
                body=render_to_string('uncon/wiki_template.md'),
                comment='Automatically generated for conference session',
            )
        
        else:
            self.article.title = title
            
        self.article.save()
        
        super(Session, self).save(**kwargs)

#
# status update and social media models
#

class Summize(models.Model):
    value = models.CharField(max_length=255)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('value',)
    
    def __unicode__(self):
        return self.value
    
    def max_id(self):
        res = self.tweets.aggregate(Max('twitter_id'))
        return res['twitter_id__max'] or 0

class Twitterer(models.Model):
    twitter_id = models.CharField(max_length=64, unique=True)
    screen_name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=128, blank=True)
    avatar_url = models.URLField(verify_exists=False)
    
    class Meta:
        ordering = ('screen_name',)
    
    def __unicode__(self):
        return self.screen_name

class Tweet(models.Model):
    summize = models.ForeignKey(Summize, related_name="tweets")
    twitter_id = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(Twitterer, related_name="tweets")
    content = models.TextField()
    timestamp = models.DateTimeField()
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return u"%s: %s" % (self.user.screen_name, self.content)

#
# Flickr
#

class FlickrPhoto(models.Model):
    flickr_id = models.CharField(max_length=64, unique=True)
    owner = models.CharField(max_length=64)
    secret = models.CharField(max_length=32)
    server = models.CharField(max_length=8)
    farm = models.CharField(max_length=8)
    title = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('-id',)
    
    def __unicode__(self):
        return self.title
