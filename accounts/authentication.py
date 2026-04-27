from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    """Беспарольный серверный процессор аутентификации"""

    def authenticate(self, request=None, uid=None, **kwargs):
        """Аутентифицировать"""
        if uid is None:
            return None
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, user_id):
        """Получить пользователя"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
