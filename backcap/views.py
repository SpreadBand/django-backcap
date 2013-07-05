# -*- coding: utf-8 -*-

# Backcap, a support module for community-driven django websites
# Copyright (C) 2010, Guillaume Libersat <guillaume@spreadband.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from backcap.settings import BACKCAP_INDEX_FEEDBACKS

if BACKCAP_INDEX_FEEDBACKS:
    from haystack.query import SearchQuerySet

import notification.models as notification
from voting.views import vote_on_object

from .models import Feedback
from .forms import FeedbackNewForm, FeedbackEditForm
from .signals import feedback_updated as sig_feedback_updated
from .sql import SumWithDefault
from .settings import BACKCAP_NOTIFIED_USERS, BACKCAP_NOTIFY_WHOLE_STAFF
from .utils import subscribe_user, unsubscribe_user

@login_required
def feedback_new(request, template_name='backcap/feedback_new.html'):
    """
    Create a new feedback
    """
    referer = request.GET.get("referer", None)

    if request.method == 'POST':
        feedback_form = FeedbackNewForm(request.POST, prefix='backcap')

        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            messages.success(request, _("Thanks for your feedback !"))

            users_to_notify = User.objects.none()
            # Add the specified users
            if BACKCAP_NOTIFIED_USERS:
                users_to_notify |= User.objects.filter(username__in=BACKCAP_NOTIFIED_USERS)

            # Add the whole staff if enabled
            if BACKCAP_NOTIFY_WHOLE_STAFF:
                users_to_notify |= User.objects.filter(is_staff=True)

            # Send notification
            notification.send(users_to_notify, "feedback_new", {'feedback': feedback})

            subscribe_user(request.user, feedback)

            return redirect(feedback)
    else:
        feedback_form = FeedbackNewForm(initial={'referer': referer}, prefix='backcap')

    return render_to_response(template_name=template_name,
                              dictionary={'feedback_form': feedback_form},
                              context_instance=RequestContext(request)
                              )

# XXX: Security problem: any user can update a feedback atm.
class FeedbackUpdateView(UpdateView):
    """
    Edit a single feedback
    """
    model = Feedback
    form_class = FeedbackEditForm
    pk_url_kwarg = 'feedback_id'
    template_name='backcap/feedback_update.html'    

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FeedbackUpdateView, self).dispatch(request, *args, **kwargs)



class FeedbackListView(ListView):
    """
    Display all the feedbacks
    """
    template_name = 'backcap/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 15
    
    def get_queryset(self, qtype='all', *args, **kwargs):
        queryset = Feedback.objects.exclude(status__in=('C', 'D', 'I', 'W')).annotate(score=SumWithDefault('votes__vote', default=0))

        self.order = self.request.GET.get('order', 'score')
        if self.order == 'newest':
            queryset = queryset.order_by('modified_on', 'kind', '-score')
        else:
            queryset = queryset.order_by('-score', 'modified_on', 'kind')
            
        if self.request.user.is_authenticated():
            # Feedbacks assigned to the user
            mine = self.request.GET.get('mine', False)
            if mine:
                queryset = queryset.filter(assigned_to=self.request.user)
                
            # Feedbacks followed by the user
            followed = self.request.GET.get('followed', False)
            if followed:
                queryset = queryset.filter(followers__user=self.request.user)

        self.qtype = qtype                
        if qtype in [choice[0] for choice in Feedback.KIND_CHOICES]:
            queryset = queryset.filter(kind=qtype)
            
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(FeedbackListView, self).get_context_data(*args, **kwargs)
        
        context['qtype'] = self.qtype
        context['order'] = self.order
        
        return context

class FeedbackDetailView(DetailView):
    """
    Shows a single feedback
    """
    model = Feedback
    pk_url_kwarg = 'feedback_id'
    template_name = 'backcap/feedback_detail.html'
    context_object_name = 'feedback'
    

# XXX Security
@login_required
def feedback_close(request, feedback_id):
    """
    Closes a feedback. This means it has been resolved.
    """
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Close it, then save
    feedback.status = 'C'
    feedback.save()

    return redirect(feedback)

@login_required
def feedback_vote(request, feedback_id, direction):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Auto (un)subscribe user if he/she's interested in this issue or not
    if direction == 'up':
        subscribe_user(request.user, feedback)
    elif direction in ('down', 'clear'):
        unsubscribe_user(request.user, feedback)

    return vote_on_object(request,
                          model=Feedback,
                          direction=direction,
                          object_id=feedback_id,
                          template_object_name='vote',
                          template_name='kb/link_confirm_vote.html',
                          allow_xmlhttprequest=True)


@login_required
def feedback_ping_observers(request, feedback_id):
    """
    Ping users that are observing this feedback
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()

    feedback = get_object_or_404(Feedback, id=feedback_id)

    notification.send(feedback.followers.all(),
                      "feedback_updated",
                      {'feedback': feedback},
                      )

    messages.success(request, _("The followers have been successfully notified"))

    return redirect(feedback)
    

def feedback_tab(request):
    return feedback_new(request,
                        template_name='backcap/feedback_tab.html')


@require_GET
def feedback_search(request, limit=10):
    query = request.GET['q']

    results = SearchQuerySet().models(Feedback).filter_or(content=query)
    if limit:
        results = results[:int(limit)]

    return render_to_response(template_name='backcap/feedback_search.html',
                              dictionary={'results': results,
                                          'query': query},
                              )

@login_required
@require_POST
def feedback_follow(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)

    subscribe_user(request.user, feedback)

    messages.success(request, _("You are now following this feedback"))

    return redirect(feedback)


@login_required
@require_POST
def feedback_unfollow(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)

    unsubscribe_user(request.user, feedback)

    messages.success(request, _("You are no more following this feedback"))

    return redirect(feedback)
    
