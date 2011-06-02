from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min
from transparencycamp.uncon.models import Conference, Session
import datetime

class Command(BaseCommand):
    help = "reset the date of the conference"
    
    def handle(self, *args, **options):
        
        con = Conference.objects.current_conference()
        
        dates = set(Session.objects.values_list('date', flat=True))
        diff = min(dates) - datetime.date(2011, 4, 30)
        
        for date in dates:
            new_date = date - diff
            Session.objects.filter(conference=con, date=date).update(date=new_date)
            
        