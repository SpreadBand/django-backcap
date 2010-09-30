from django.conf.urls.defaults import patterns, url
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',             
    url(r'^new$', views.feedback_new, name='feedback-new'),
    url(r'^list$', views.feedback_list, name='feedback-list'),
    url(r'^list/(?P<qtype>\w+)$', views.feedback_list, name='feedback-list'),
    url(r'^search$', views.feedback_search, name='feedback-search'),
    url(r'^(?P<feedback_id>\d+)/$', views.feedback_detail, name='feedback-detail'),
    url(r'^(?P<feedback_id>\d+)/update$', views.feedback_update, name='feedback-update'),
    url(r'^(?P<feedback_id>\d+)/close$', views.feedback_close, name='feedback-close'),
    url(r'^(?P<feedback_id>\d+)/ping$', views.feedback_ping_observers, name='feedback-ping-observers'),

    url(r'^feedback-tab$', views.feedback_tab, name='feedback-tab'),

    # Votes
    url(r'^(?P<feedback_id>\d+)/(?P<direction>up|down|clear)vote/?$', views.feedback_vote, name='feedback-vote'),

)




