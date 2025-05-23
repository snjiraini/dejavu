from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User, Role
from .decorators import role_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .api_docs import login_docs

@csrf_exempt
@require_http_methods(["POST"])
@login_docs
def login_user(request):
    """API endpoint for user login"""
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'username': user.username,
            'roles': list(user.roles.values_list('name', flat=True))
        })
    else:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

@require_http_methods(["POST"])
def logout_user(request):
    """API endpoint for user logout"""
    logout(request)
    return JsonResponse({'success': True})

@csrf_exempt
@require_http_methods(["POST"])
@role_required(['superuser'])
def create_user(request):
    """API endpoint for user creation (superuser only)"""
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role_names = data.get('roles', [])
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Assign roles
    for role_name in role_names:
        try:
            role = Role.objects.get(name=role_name)
            user.roles.add(role)
        except Role.DoesNotExist:
            pass
    
    return JsonResponse({
        'success': True,
        'user_id': user.id,
        'username': user.username,
        'roles': list(user.roles.values_list('name', flat=True))
    }, status=201)

@csrf_exempt
@require_http_methods(["GET"])
@role_required(['superuser'])
def list_users(request):
    """API endpoint to list all users (superuser only)"""
    users = User.objects.all()
    data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'roles': list(user.roles.values_list('name', flat=True)),
        'date_joined': user.date_joined
    } for user in users]
    
    return JsonResponse({'users': data})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Get authenticated user info from JWT token"""
    if request.user.is_authenticated:
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'roles': list(request.user.roles.values_list('name', flat=True)),
            'is_superuser': request.user.is_superuser
        })
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED) 