from django.contrib.auth.models import User


def deactivate_user_profile(user):
    user.is_active = False
    user.save()


def deactivate_staff_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return True
    except User.DoesNotExist:
        return False
