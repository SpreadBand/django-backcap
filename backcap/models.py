from django.db import models
from django.db.models import ForeignKey, CharField, TextField, DateTimeField
from django.db.models import PositiveIntegerField, BooleanField, IntegerField
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from voting.models import Vote

from .signals import feedback_updated

class Feedback(models.Model):
    class Meta:
        ordering = ('-modified_on', 'kind')

    KIND_CHOICES = (
        ('Q', _('Question')),
        ('P', _('Problem')),
        ('I', _('Idea')),
        )

    STATUS_CHOICES = (
        ('N', _('New (unreviewed)')),
        ('V', _('Valid')),
        ('M', _('Need more information')),
        ('W', _('Won\'t Fix')),
        ('I', _('Invalid')),
        ('A', _('Assigned')),
        ('D', _('Duplicate')),
        ('R', _('Re-opened')),
        ('C', _('Closed')),
        )

    # Timestamps
    created_on = DateTimeField(auto_now_add=True)
    modified_on = DateTimeField(auto_now=True)

    # Who and what
    user = ForeignKey(User)
    referer = TextField(verbose_name=_('Referer'),
                        blank=True,
                        null=True)

    # Contents
    kind = CharField(verbose_name=_('Kind'),
                     max_length=1, choices=KIND_CHOICES)
    title = CharField(verbose_name=_('Title'),
                      max_length=255)
    text = TextField(verbose_name=_('Text'),
                     help_text=_("Description of the feedback"))

    # State
    status = CharField(verbose_name=_('Status'),
                       max_length=1,
                       choices=STATUS_CHOICES, default='N')
         
    assigned_to = ForeignKey(User,
                             verbose_name=_('Assigned to'),
                             limit_choices_to = {'is_staff': True},
                             related_name='assigned_feedbacks',
                             null=True,
                             blank=True)

    duplicate_of = ForeignKey('self',
                              verbose_name=_('Duplicate of'),
                              related_name='duplicates',
                              null=True,
                              blank=True)

    votes = generic.GenericRelation(Vote,
                                    object_id_field="object_id",
                                    content_type_field="content_type")


    def __unicode__(self):
        return '%s - %s' % (self.kind, self.title)


    @models.permalink
    def get_absolute_url(self):
        return ('backcap:feedback-detail', (), {'feedback_id': self.id})
    

## Signal routing
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.signals import comment_was_posted
from annoying.decorators import signals
import notification.models as notification

@signals(feedback_updated)
def on_feedback_updated(sender, *args, **kwargs):
    notification.send_observation_notices_for(sender, 'feedback_updated', {'feedback': sender})

@signals(comment_was_posted)
def on_comment_posted(sender, comment, request, *args, **kwargs):
    feedback_ctype = ContentType.objects.get_for_model(Feedback)
    if comment.content_type == feedback_ctype:
        feedback_updated.send(sender=comment.content_object)
