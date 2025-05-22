#!/bin/bash

# Set default password
PASSWORD="testpassword123"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--password)
      PASSWORD="$2"
      shift 2
      ;;
    -o|--overwrite)
      OVERWRITE="--overwrite"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "Setting up Dejavu users..."
echo "-------------------------"

# First ensure roles are created
echo "Creating roles..."
python manage.py create_roles_and_users

# Then create one user per role
echo -e "\nCreating test users..."
python manage.py create_test_users --password "$PASSWORD" $OVERWRITE

echo -e "\nSetup complete!"
echo "You can now log in to the frontend with any of the above users."
echo "The password for all users is: $PASSWORD" 