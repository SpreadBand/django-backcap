from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site

from .models import Feedback

class FeedbackIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        return Feedback.objects.all()


site.register(Feedback, FeedbackIndex)




