import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shore.settings')
django.setup()

from myapp.models import Login, UserProfile

print("--- Simulating Registration Logic ---")

test_email = "debug_user_v2@test.com"
test_password = "password123"
test_name = "Debug User"
test_phone = "1234567890"
test_address = "123 Debug Lane"

# Cleanup previous test if exists
try:
    existing = Login.objects.get(username=test_email)
    print(f"Deleting existing test user: {existing}")
    existing.delete()
except Login.DoesNotExist:
    pass

try:
    print("1. Creating Login...")
    user = Login.objects.create_user(
        username=test_email,
        password=test_password,
        usertype="user",
        viewpassword=test_password
    )
    print(f"   Login created: ID={user.id}")

    print("2. Creating UserProfile...")
    profile = UserProfile.objects.create(
        logid=user,
        name=test_name,
        email=test_email,
        phone=test_phone,
        address=test_address
    )
    print(f"   UserProfile created: ID={profile.id}")
    
    print("--- Verification ---")
    p_check = UserProfile.objects.get(logid=user)
    print(f"   Retrieved Profile: {p_check.name}, {p_check.address}")
    
except Exception as e:
    print(f"!!! ERROR: {e}")
    import traceback
    traceback.print_exc()
