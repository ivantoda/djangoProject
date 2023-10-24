from django.contrib.auth.hashers import check_password 
from app_1.models import CustomUser

class Validate:
    def authenticate_user(usrnm, psswrd):
        try:
            user = CustomUser.objects.filter(username=usrnm).first()
            if user is None:
                return None
            else:
                if check_password(psswrd, user.password):
                    return user
                else:
                    return None
        except CustomUser.DoesNotExist:
            return None