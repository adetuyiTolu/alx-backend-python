from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

nested_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet,
                       basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
