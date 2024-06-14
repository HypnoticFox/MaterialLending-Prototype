from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(
    *group_names,
    login_url=None
):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
            else:
                raise PermissionDenied
        return False
    
    return user_passes_test(
        in_groups,
        login_url=login_url
    )