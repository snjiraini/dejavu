from django.core.management.base import BaseCommand
from django.db import transaction
from fingerprinting.models import User, Role
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates one test user for each role in the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            default='password123',
            help='Password to use for all test users (default: password123)',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing users if they already exist',
        )

    def handle(self, *args, **options):
        password = options['password']
        overwrite = options['overwrite']
        
        # Get all roles from the system
        roles = Role.objects.all()
        
        if not roles.exists():
            self.stdout.write(self.style.ERROR('No roles found in the system. Please run create_roles_and_users command first.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Creating test users with password: {password}'))
        
        # Create one user for each role
        with transaction.atomic():
            # Create a superuser
            try:
                if User.objects.filter(username='admin').exists():
                    if overwrite:
                        User.objects.filter(username='admin').delete()
                        self.stdout.write(self.style.WARNING('Deleted existing admin user'))
                    else:
                        self.stdout.write(self.style.WARNING('Admin user already exists, skipping'))
                
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@example.com',
                        password=password
                    )
                    self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create admin user: {str(e)}'))
            
            # Create one user for each role
            for role in roles:
                username = role.name.lower()
                email = f'{username}@example.com'
                
                try:
                    if User.objects.filter(username=username).exists():
                        if overwrite:
                            User.objects.filter(username=username).delete()
                            self.stdout.write(self.style.WARNING(f'Deleted existing user: {username}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'User {username} already exists, skipping'))
                            continue
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.roles.add(role)
                    self.stdout.write(self.style.SUCCESS(f'Created user: {username} with role: {role.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create user {username}: {str(e)}'))
            
            # Create a user with multiple roles
            try:
                if User.objects.filter(username='multi_role').exists():
                    if overwrite:
                        User.objects.filter(username='multi_role').delete()
                        self.stdout.write(self.style.WARNING('Deleted existing multi_role user'))
                    else:
                        self.stdout.write(self.style.WARNING('Multi-role user already exists, skipping'))
                else:
                    user = User.objects.create_user(
                        username='multi_role',
                        email='multi_role@example.com',
                        password=password
                    )
                    # Add the first 3 roles to this user
                    for role in roles[:3]:
                        user.roles.add(role)
                    
                    role_names = ', '.join([r.name for r in roles[:3]])
                    self.stdout.write(self.style.SUCCESS(f'Created multi-role user with roles: {role_names}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create multi-role user: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('All test users created successfully!'))
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS('User credentials summary:'))
        self.stdout.write(f'Admin: username=admin, password={password}')
        
        for role in roles:
            username = role.name.lower()
            self.stdout.write(f'{role.name}: username={username}, password={password}')
        
        self.stdout.write(f'Multi-role user: username=multi_role, password={password}') 