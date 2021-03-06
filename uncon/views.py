import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_detail, object_list
from transparencycamp.uncon.models import Session, Conference
from markupwiki.models import Article
from markupwiki.views import view_article


def session_detail(request, pk, template_name=None):
    sessions = Session.objects.all()
    kwargs = {
        'queryset': sessions,
        'object_id': pk,
    }
    if template_name:
        kwargs['template_name'] = template_name
    return object_detail(request, **kwargs)


def session_list(request, con_slug=None, template_name=None):
    conference = Conference.objects.current().order_by('-start_date')[0]
    sessions = Session.objects.filter(conference__slug=con_slug or conference.slug)
    try:
        conference = sessions[0].conference
    except:
        pass
    kwargs = {
        'queryset': sessions,
        'extra_context': {
            'conference': conference,
            'current_date': datetime.date.today(),
        }
    }
    if template_name:
        kwargs['template_name'] = template_name
    return object_list(request, **kwargs)


def wiki_redirect(request, day, title):
    title = "2011/dc/%s/%s" % (day, title)
    if 'noredirect' not in request.GET:
        session = Session.objects.get(article__title=title)
        return HttpResponseRedirect('/sessions/%s/' % session.pk)
    return view_article(request, title)
