from django.template import Library, Node

from backcap.models import Feedback

register = Library()

@register.tag
def get_feedbacks(parser, token):
    """
    {% get_feedbacks %}
    """
    return FeedbackNode()
    
class FeedbackNode(Node):
    def render(self, context):
        context['feedbacks'] = Feedback.objects.all()
        return ''
