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

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    def view(self, obj):
        return "<a href='%s'>View</a>" % obj.get_absolute_url()
    view.allow_tags = True
    
    list_display = ['title', 'kind', 'user', 'modified_on', 'view']
    search_fields = ['user', 'text']
    list_filter = ['kind', 'created_on', 'modified_on']
    
    def get_urls(self):
        urls = super(FeedbackAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^view/(?P<feedback_id>\d+)/$', self.admin_site.admin_view(self.view_feedback), name='view-feedback'),
        )
        return my_urls + urls
        
    def view_feedback(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        return render_to_response('backcap/admin/view_feedback.html',
                                  {'feedback': feedback}, 
                                  context_instance=RequestContext(request)
                                  )

admin.site.register(Feedback, FeedbackAdmin)

admin.site.index_template = 'backcap/admin/index.html'



