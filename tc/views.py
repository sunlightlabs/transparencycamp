from django.shortcuts import render_to_response
from django.template import RequestContext
from transparencycamp.uncon.models import Conference, Session


def index(request):
    con = Conference.objects.current_conference()
    next = {
        'time': con.next_timeslot(),
        'sessions': con.next_sessions(),
    }
    return render_to_response("index.html",
                              {'next': next},
                              context_instance=RequestContext(request))


def live(request):
    return render_to_response("live.html",
                              context_instance=RequestContext(request))
