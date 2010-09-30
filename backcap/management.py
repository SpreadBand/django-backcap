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

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

import notification.models as notification

from annoying.decorators import signals

@signals(post_syncdb, sender=notification)
def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("feedback_new", _("New feedback"), _("A new feedback was submitted"))
    notification.create_notice_type("feedback_updated", _("Feedback updated"), _("A feedback was updated"))

    





