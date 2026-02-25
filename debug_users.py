import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shore.settings')
django.setup()

from myapp.models import Login, UserProfile

print("--- Database Diagnostic ---")
users = Login.objects.filter(usertype='user')
print(f"Total Logins with usertype='user': {users.count()}")

profiles = UserProfile.objects.all()
print(f"Total UserProfiles: {profiles.count()}")

orphans = []
for u in users:
    if not UserProfile.objects.filter(logid=u).exists():
        orphans.append(u.username)

print(f"Orphaned Users (No Profile): {len(orphans)}")
if orphans:
    print("Example orphans:", orphans[:5])
else:
    print("All users have profiles.")
