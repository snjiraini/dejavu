from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from . import api_auth
from . import api_catalog

app_name = 'fingerprinting'

urlpatterns = [
    path('', views.index, name='index'),
    path('recognize/', views.recognize_audio, name='recognize_audio'),
    path('fingerprint/', views.fingerprint_song, name='fingerprint_song'),
    
    # JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/auth/login/', api_auth.login_user, name='login'),
    path('api/auth/logout/', api_auth.logout_user, name='logout'),
    path('api/auth/users/', api_auth.create_user, name='create_user'),
    path('api/auth/users/list/', api_auth.list_users, name='list_users'),
    path('api/auth/me/', api_auth.user_info, name='user_info'),
    
    path('api/catalog/tracks/', api_catalog.track_list, name='track_list'),
    path('api/catalog/tracks/<uuid:track_id>/', api_catalog.track_detail, name='track_detail'),
] 