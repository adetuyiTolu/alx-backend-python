from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

nested_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet,
                       basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
