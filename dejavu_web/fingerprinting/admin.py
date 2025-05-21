from django.contrib import admin
from .models import (
    User, Role, Track, Album, Artist, ArtistGroup, 
    ArtistGroupMember, TrackArtist, AudioFile, 
    Fingerprint, RadioStation, RadioAirplayLog
)

# Register custom User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'get_roles')
    filter_horizontal = ('roles',)
    search_fields = ('username', 'email')
    
    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = 'Roles'

# Register Role model
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Register Track model
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'duration', 'isrc', 'created_at')
    search_fields = ('title', 'isrc')
    list_filter = ('created_at',)

# Register Album model
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('release_date', 'created_at')

# Register Artist model
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    search_fields = ('name',)
    list_filter = ('type', 'created_at')

# Register ArtistGroup model
@admin.register(ArtistGroup)
class ArtistGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created_at')
    search_fields = ('group_name',)

# Register ArtistGroupMember model
@admin.register(ArtistGroupMember)
class ArtistGroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'artist')
    list_filter = ('group',)

# Register TrackArtist model
@admin.register(TrackArtist)
class TrackArtistAdmin(admin.ModelAdmin):
    list_display = ('track', 'artist', 'role')
    list_filter = ('role',)
    search_fields = ('track__title', 'artist__name')

# Register AudioFile model
@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('track', 'format', 'bitrate', 'created_at')
    list_filter = ('format', 'created_at')
    search_fields = ('track__title',)

# Register Fingerprint model (read-only)
@admin.register(Fingerprint)
class FingerprintAdmin(admin.ModelAdmin):
    list_display = ('track', 'hash', 'offset', 'date_created')
    search_fields = ('track__title', 'hash')
    list_filter = ('date_created',)
    readonly_fields = ('track', 'hash', 'offset', 'date_created', 'date_modified')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# Register RadioStation model
@admin.register(RadioStation)
class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

# Register RadioAirplayLog model
@admin.register(RadioAirplayLog)
class RadioAirplayLogAdmin(admin.ModelAdmin):
    list_display = ('station', 'track', 'played_at', 'confidence_score', 'created_at')
    search_fields = ('station__name', 'track__title')
    list_filter = ('station', 'played_at', 'created_at')
