import notification.models as notification

def subscribe_user(user, feedback):
    """
    Subscribe a user to any change of a given feedback
    """
    if not notification.is_observing(feedback, user, signal='feedback_updated'):
        notification.observe(feedback, user, 'feedback_updated', 'feedback_updated')

def unsubscribe_user(user, feedback):
    """
    Unsubscribe a user to any change of a given feedback
    """
    if notification.is_observing(feedback, user, signal='feedback_updated'):
        notification.stop_observing(feedback, user, 'feedback_updated')
    





