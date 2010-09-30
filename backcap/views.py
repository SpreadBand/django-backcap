from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.generic.create_update import update_object
from django.views.generic.list_detail import object_list, object_detail
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET

from haystack.query import SearchQuerySet
import notification.models as notification
from voting.views import vote_on_object

from .models import Feedback
from .forms import FeedbackNewForm, FeedbackEditForm
from .signals import feedback_updated as sig_feedback_updated
from .sql import SumWithDefault

@login_required
def feedback_new(request, template_name='backcap/feedback_new.html'):
    """
    Create a new feedback
    """
    referer = request.GET.get("referer", None)

    if request.method == 'POST':
        feedback_form = FeedbackNewForm(request.POST)

        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            messages.success(request, _("Thanks for you feedback !"))

            staff = User.objects.filter(is_staff=True)
            notification.send(staff, "feedback_new", {'feedback': feedback})
            notification.observe(feedback, request.user, "feedback_updated", "feedback_updated")

            return redirect(feedback)
    else:
        feedback_form = FeedbackNewForm(initial={'referer': referer})

    return render_to_response(template_name=template_name,
                              dictionary={'feedback_form': feedback_form},
                              )

# XXX: Security
@login_required
def feedback_update(request, feedback_id):
    """
    Edit a single feedback
    """
    return update_object(request,
                         form_class=FeedbackEditForm,
                         object_id=feedback_id,
                         template_name='backcap/feedback_update.html',
                         )

def feedback_list(request, qtype='all'):
    """
    Display all the feedbacks
    """
    queryset = Feedback.objects.exclude(status__in=('C', 'D', 'I')).annotate(score=SumWithDefault('votes__vote', default=0))

    order = request.GET.get('order', 'score')
    if order == 'newest':
        quersyet = queryset.order_by('modified_on', 'kind', '-score')
    else:
        queryset = queryset.order_by('-score', 'modified_on', 'kind')


    if qtype in [choice[0] for choice in Feedback.KIND_CHOICES]:
        queryset = queryset.filter(kind=qtype)

    return object_list(request,
                       queryset=queryset,
                       template_name='backcap/feedback_list.html',
                       template_object_name='feedback',
                       paginate_by=15,
                       extra_context={'qtype': qtype,
                                      'order': order},
                       )

def feedback_detail(request, feedback_id):
    """
    Shows a single feedback
    """
    return object_detail(request,
                         queryset=Feedback.objects.all(),
                         object_id=feedback_id,
                         template_object_name='feedback',
                         template_name='backcap/feedback_detail.html',
                         )

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
    is_observing = notification.is_observing(feedback, request.user, "feedback_updated")
    if direction == 'up' and not is_observing:
        notification.observe(feedback, request.user, "feedback_updated", "feedback_updated")
    elif direction in ('down', 'clear') and is_observing:
        notification.stop_observing(feedback, request.user, "feedback_updated")

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
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    feedback = get_object_or_404(Feedback, id=feedback_id)

    notification.send([feedback.user],
                      "feedback_updated",
                      {'feedback': feedback},
                      )

    messages.success(request, _("The users have been successfully notified"))

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
