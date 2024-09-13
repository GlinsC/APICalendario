from django.urls import path
from .views import CreateEventView, DeleteEventView



urlpatterns = [
    path('events/', CreateEventView.as_view(), name='create-event'),
    path('events/<str:event_id>/', DeleteEventView.as_view(), name='delete-event'),
]