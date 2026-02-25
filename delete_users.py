import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shore.settings')
django.setup()

from myapp.models import Login, UserProfile

print("--- Deleting User Data ---")

# Delete all users with usertype='user'
users_to_delete = Login.objects.filter(usertype='user')
count = users_to_delete.count()

if count > 0:
    print(f"Found {count} users to delete.")
    users_to_delete.delete()
    print("Successfully deleted all 'user' accounts.")
else:
    print("No 'user' accounts found to delete.")

# Double check profiles (should be cascaded delete, but good to verify)
profiles = UserProfile.objects.all()
print(f"Remaining UserProfiles: {profiles.count()}")
