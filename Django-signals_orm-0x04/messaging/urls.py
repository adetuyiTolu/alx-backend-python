from django.urls import path
from .views import delete_user, inbox

urlpatterns = [
    path('delete_account/', delete_user, name='delete_account'),
    path('inbox/', inbox, name='inbox'),
]
