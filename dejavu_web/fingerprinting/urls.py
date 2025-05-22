from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from . import api_auth
from . import api_catalog
from . import api_monitoring

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
    
    # Catalog API
    path('api/catalog/tracks/', api_catalog.track_list, name='track_list'),
    path('api/catalog/tracks/<uuid:track_id>/', api_catalog.track_detail, name='track_detail'),
    path('api/catalog/albums/', api_catalog.album_list, name='album_list'),
    path('api/catalog/albums/<uuid:album_id>/', api_catalog.album_detail, name='album_detail'),
    path('api/catalog/artists/', api_catalog.artist_list, name='artist_list'),
    path('api/catalog/artists/<uuid:artist_id>/', api_catalog.artist_detail, name='artist_detail'),
    path('api/catalog/audio-files/', api_catalog.audio_file_list, name='audio_file_list'),
    path('api/catalog/audio-files/<uuid:audio_file_id>/', api_catalog.audio_file_detail, name='audio_file_detail'),
    
    # Monitoring API
    path('api/monitoring/airplay-logs/', api_monitoring.airplay_logs, name='airplay_logs'),
    path('api/monitoring/airplay-logs/<uuid:log_id>/', api_monitoring.airplay_log_detail, name='airplay_log_detail'),
    path('api/monitoring/airplay-logs/create/', api_monitoring.create_airplay_log, name='create_airplay_log'),
    path('api/monitoring/airplay-logs/<uuid:log_id>/delete/', api_monitoring.delete_airplay_log, name='delete_airplay_log'),
    path('api/monitoring/stations/', api_monitoring.station_list, name='station_list'),
    path('api/monitoring/stations/<uuid:station_id>/', api_monitoring.station_detail, name='station_detail'),
] 