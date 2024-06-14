from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    # Disables normal sign up.
    def is_open_for_signup(self, request):
        return False

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        if sociallogin.user.email.endswith(f"@{settings.STAFF_EMAIL_DOMAIN}"):
            return True
        
        return False
    
    # Runs on each login and initial signup.
    def populate_user(self, request, sociallogin, data):
        
        # Change data before creating user object.
        
        # Create user object.
        user = super().populate_user(request, sociallogin, data)
        
        # Do stuff before returning user.
        
        return user

    # Runs only the first time a user logs in.
    def save_user(self, request, sociallogin, form=None):
        
        # Change data before creating new user object.
        
        # Create new user object.
        new_user = super().save_user(request, sociallogin, form)
        
        # Do stuff before saving new user.
        if new_user.email.endswith(f"@{settings.STAFF_EMAIL_DOMAIN}"):
            group = Group.objects.get(name=settings.STAFF_GROUP_NAME)
            new_user.groups.add(group)
        
        return new_user
