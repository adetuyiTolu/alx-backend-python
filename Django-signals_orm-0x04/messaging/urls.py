from django.urls import path
from .views import delete_user, inbox, unread_inbox

urlpatterns = [
    path('delete_account/', delete_user, name='delete_account'),
    path('inbox/', inbox, name='inbox'),
    path('unread/', unread_inbox, name='unread_inbox'),
]
