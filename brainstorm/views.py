import json
import datetime

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse
from django.views.generic import list_detail
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from brainstorm.models import Subsite, Idea, Vote
from brainstorm.forms import IdeaForm


def idea_list(request, slug, ordering='most_popular', **kwargs):
    subsite = get_object_or_404(Subsite, slug=slug)
    ordering_db = {'most_popular': '-score',
                   'latest': '-timestamp'}.get(ordering, ordering)
    qs = Idea.objects.with_user_vote(request.user).filter(subsite__slug=slug, is_public=True).select_related().order_by(ordering_db)
    form = kwargs.get('form', IdeaForm(request))
    if hasattr(qs, '_gatekeeper'):
        qs = qs.approved()
    return list_detail.object_list(request, queryset=qs,
        extra_context={'ordering': ordering, 'subsite': subsite, 'form': form},
        paginate_by=subsite.ideas_per_page,
        template_object_name='idea')


def idea_detail(request, slug, id):
    idea = get_object_or_404(Idea.objects.with_user_vote(request.user), pk=id, subsite__slug=slug, is_public=True)
    return render_to_response('brainstorm/idea_detail.html',
                              {'idea': idea,
                               'subsite': idea.subsite,
                               'is_permalink': True, },
                              context_instance=RequestContext(request))


@require_POST
def new_idea(request, slug):
    subsite = get_object_or_404(Subsite, pk=slug)
    if not subsite.user_can_post(request.user):
        return redirect(subsite.get_absolute_url())
    form = IdeaForm(request, request.POST)
    request.session['name'] = form['name'].value()
    request.session['email'] = form['email'].value()
    if form.is_valid():
        data = form.cleaned_data
        data['subsite'] = subsite
        if not request.user.is_anonymous:
            data['user'] = request.user
        idea = Idea.objects.create(**data)
        return redirect(idea)
    else:
        import pdb; pdb.set_trace()
        ctx = {'subsite': subsite, 'form': form}
        return render(request, 'brainstorm/idea_form.html', ctx)


@require_POST
@login_required
def vote(request, slug, id, format='html'):
    idea_id = int(id)
    vote = int(request.POST.get('vote'))
    if vote not in (-1, 0, 1):
        vote = 0
    idea = get_object_or_404(Idea, pk=idea_id, subsite__slug=slug)
    vobj, new = Vote.objects.get_or_create(user=request.user, idea=idea,
                                               defaults={'value': vote})

    if not vote:
        vobj.delete()
    elif not new:
        vobj.value = vote
        vobj.save()

    idea = Idea.objects.with_user_vote(request.user).get(pk=idea_id,
                                                         subsite__slug=slug)

    if format is 'json':
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        response_d = {
            'success': True,
            'slug': idea.subsite.slug,
            'id': idea.id,
            'vote': vote,
            'score': idea.score,
            'upvotes': idea.upvotes_label.format(idea.upvotes),
            'downvotes': idea.downvotes_label.format(idea.downvotes),
            'timestamp': vobj.timestamp,
        }
        return HttpResponse(json.dumps(response_d, default=dthandler), content_type="application/json")

    if request.is_ajax():
        return render_to_response('brainstorm/partials/idea_vote.html',
            {'idea': idea, 'subsite': idea.subsite},
            context_instance=RequestContext(request))

    return redirect(idea)
