from django.http import JsonResponse
from functools import wraps

def role_required(roles):
    """
    Decorator for views that checks if the user has any of the specified roles.
    If superuser, access is always granted.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Superusers always have access
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has any of the required roles
            if hasattr(request.user, 'roles'):
                for role in roles:
                    if request.user.has_role(role):
                        return view_func(request, *args, **kwargs)
            
            return JsonResponse({'error': 'Access forbidden. Required roles: ' + ', '.join(roles)}, status=403)
        return wrapped_view
    return decorator 