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

