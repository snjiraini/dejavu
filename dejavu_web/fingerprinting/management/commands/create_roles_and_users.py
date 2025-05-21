from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fingerprinting.models import Role, Artist

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default roles and a superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for the superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='adminpassword',
            help='Password for the superuser',
        )

    def handle(self, *args, **options):
        # Create the roles
        roles = [
            ('catalog_admin', 'Catalog Administrator', 'Manages artist, track, and album metadata; uploads audio files and lyrics'),
            ('rights_holder', 'Rights Holder', 'Assigns ownership/royalty splits; registers ISRC codes; views royalty reports'),
            ('radio_monitor', 'Radio Monitor', 'Monitors radio matches; investigates unlicensed usage; confirms detections'),
            ('developer', 'Developer/Engineer', 'Integrates audio matching engine; maintains fingerprinting system; handles backend scalability'),
            ('analyst', 'Business Analyst', 'Generates reports by station/artist/region; uses aggregated insights for marketing/licensing'),
            ('artist', 'Artist', 'May access a dashboard to view plays, revenue, exposure'),
            ('label', 'Label', 'May access a dashboard to view plays, revenue, exposure'),
            ('superuser', 'Super User', 'Has access to all functionality'),
        ]
        
        for role_name, role_display, description in roles:
            Role.objects.get_or_create(
                name=role_name,
                defaults={'description': description}
            )
            self.stdout.write(self.style.SUCCESS(f'Created role: {role_display}'))
        
        # Create a superuser if it doesn't exist
        username = options['username']
        email = options['email']
        password = options['password']
        
        if not User.objects.filter(username=username).exists():
            superuser = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            # Assign superuser role
            superuser_role = Role.objects.get(name='superuser')
            superuser.roles.add(superuser_role)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))

        # Create a demo artist user
        if not User.objects.filter(username='artist1').exists():
            # Create an artist
            artist, created = Artist.objects.get_or_create(
                name='Demo Artist',
                defaults={'type': 'solo', 'bio': 'Demo artist for testing purposes'}
            )
            
            # Create an artist user
            artist_user = User.objects.create_user(
                username='artist1',
                email='artist@example.com',
                password='password123'
            )
            
            # Associate with the artist
            artist_user.associated_artist = artist
            artist_user.save()
            
            # Assign artist role
            artist_role = Role.objects.get(name='artist')
            artist_user.roles.add(artist_role)
            
            self.stdout.write(self.style.SUCCESS('Successfully created artist user: artist1'))

        self.stdout.write(self.style.SUCCESS('Setup complete. You can now log in with the superuser credentials.')) 