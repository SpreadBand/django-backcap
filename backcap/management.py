from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

import notification.models as notification

from annoying.decorators import signals

@signals(post_syncdb, sender=notification)
def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("feedback_new", _("New feedback"), _("A new feedback was submitted"))
    notification.create_notice_type("feedback_updated", _("Feedback updated"), _("A feedback was updated"))

    





