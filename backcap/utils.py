import notification.models as notification

def subscribe_user(user, feedback):
    """
    Subscribe a user to any change of a given feedback
    """
    feedback.followers.add(user)

def unsubscribe_user(user, feedback):
    """
    Unsubscribe a user to any change of a given feedback
    """
    feedback.followers.remove(user)
    





