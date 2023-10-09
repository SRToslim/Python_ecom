from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model, login
from django.db.models import Q

User = get_user_model()


class UsernameOrEmail(ModelBackend):
    def authenticate(self, request, username=None, password=None, google_user_info=None, facebook_user_info=None, github_user_info=None, **kwargs):
        if google_user_info:
            try:
                user = User.objects.get(Q(email=google_user_info['email']) | Q(username=google_user_info['email']))
                return user
            except User.DoesNotExist:
                pass
        elif facebook_user_info:
            try:
                user = User.objects.get(Q(email=facebook_user_info['email']) | Q(username=facebook_user_info['email']))
                return user
            except User.DoesNotExist:
                pass
        elif github_user_info:
            try:
                user = User.objects.get(Q(email=github_user_info['email']) | Q(username=github_user_info['email']))
                return user
            except User.DoesNotExist:
                pass
        else:
            try:
                user = User.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username) | Q(membership_no__iexact=username))

            except User.DoesNotExist:
                User().set_password(password)
                return
            except User.MultipleObjectsReturned:
                user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username) | Q(
                    membership_no__iexact=username)).order_by('id').first()
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
