from django.contrib import admin
from transparencycamp.uncon.models import (
    Conference, Session, Summize, Twitterer, Tweet, FlickrPhoto)

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'start_date', 'end_date')
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Conference, ConferenceAdmin)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('title','location','date','start_time','end_time','has_wiki')
    list_editable = ('has_wiki',)
    list_filter = ('date','has_wiki')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('article',)
admin.site.register(Session, SessionAdmin)

class SummizeAdmin(admin.ModelAdmin):
    list_display = ('value', 'slug')
    prepopulated_fields = {'slug': ('value',)}
admin.site.register(Summize, SummizeAdmin)

class TwittererAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'twitter_id')
admin.site.register(Twitterer, TwittererAdmin)

class TweetAdmin(admin.ModelAdmin):
    list_filter = ('summize',)
admin.site.register(Tweet, TweetAdmin)

class FlickrPhotoAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(FlickrPhoto, FlickrPhotoAdmin)