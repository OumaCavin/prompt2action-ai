"""
WebSocket Routing for Real-Time Progress Tracking
Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/workflow/(?P<workflow_id>\w+)/$', consumers.WorkflowConsumer.as_asgi()),
    re_path(r'ws/progress/$', consumers.ProgressConsumer.as_asgi()),
]
