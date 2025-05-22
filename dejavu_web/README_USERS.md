# Dejavu Web - User Management

This document explains how to set up test users with different roles for the Dejavu system.

## Available Roles

The system has the following roles:

- `catalog_admin`: Manages artist, track, and album metadata; uploads audio files and lyrics
- `rights_holder`: Assigns ownership/royalty splits; registers ISRC codes; views royalty reports
- `radio_monitor`: Monitors radio matches; investigates unlicensed usage; confirms detections
- `developer`: Integrates audio matching engine; maintains fingerprinting system; handles backend scalability
- `analyst`: Business Analyst - Generates reports by station/artist/region; uses aggregated insights for marketing/licensing
- `artist`: May access a dashboard to view plays, revenue, exposure
- `label`: May access a dashboard to view plays, revenue, exposure
- `superuser`: Has access to all functionality

## Creating Test Users

To create test users for each role, run the provided shell script:

```bash
./create_users.sh
```

This will:

1. Create all the necessary roles if they don't exist yet
2. Create one user for each role with the username matching the role name (e.g., `catalog_admin`, `artist`, etc.)
3. Create a superuser named `admin`
4. Create a user with multiple roles named `multi_role`

### Options

You can customize the user creation with the following options:

- `-p, --password PASSWORD`: Set a custom password for all users (default: `testpassword123`)
- `-o, --overwrite`: Overwrite existing users if they already exist

Example:

```bash
./create_users.sh -p mySecurePassword -o
```

## Frontend Login

You can use any of these users to log in to the frontend:

- Username: `admin`, Password: as specified (superuser)
- Username: `catalog_admin`, Password: as specified
- Username: `rights_holder`, Password: as specified
- Username: `radio_monitor`, Password: as specified
- Username: `developer`, Password: as specified
- Username: `analyst`, Password: as specified
- Username: `artist`, Password: as specified
- Username: `label`, Password: as specified
- Username: `multi_role`, Password: as specified (has multiple roles)

## Manual User Creation

You can also create users manually using the Django management commands:

```bash
# Create roles and superuser
python manage.py create_roles_and_users

# Create one user per role
python manage.py create_test_users
```

## Testing Different Role Permissions

After creating the users, you can log in to the frontend with different usernames to test how the interface changes based on the user's role. The sidebar navigation will only show the pages that the user has permission to access.
