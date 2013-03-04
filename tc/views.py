import urlparse

from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render_to_response, render, redirect
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


def login(request):
    referer = request.META.get('HTTP_REFERER')
    try:
        path = urlparse.urlparse(referer).path
    except:
        path = None

    if referer and urlparse.urlparse(referer).netloc == request.META.get('HTTP_HOST'):
        try:
            resolve(path)
        except:
            path = None
    else:
        path = None

    if request.user.is_anonymous():
        if path:
            request.session['next'] = path
        else:
            request.session['next'] = '/'
        return render(request, 'public_login.html')
    else:
        return redirect('/logged_in/')


def logged_in(request):
    if request.user.is_staff and not request.session.get('next'):
        return redirect('/admin/')
    else:
        try:
            del request.session['next']
        except:
            pass
        return redirect(request.session.get('next', '/'))
