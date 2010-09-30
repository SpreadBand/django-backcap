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

from django import forms
from django.forms import CharField, HiddenInput, ChoiceField
from django.forms import RadioSelect

from .models import Feedback

class FeedbackNewForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('kind', 'title', 'text', 'referer')

    referer = CharField(widget=HiddenInput, required=False)
    kind = ChoiceField(widget=RadioSelect(), choices=Feedback.KIND_CHOICES)
    

class FeedbackEditForm(forms.ModelForm):
    class Meta:
        model = Feedback

    duplicate_of = forms.ModelChoiceField(queryset=Feedback.objects.all(),
                                          widget=forms.TextInput,
                                          required=False)

