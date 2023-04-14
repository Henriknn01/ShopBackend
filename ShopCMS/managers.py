from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):
   def create_user(self, email, password=None, **extra_fields):
       email = self.normalize_email(email)
       user = self.model(email=email, **extra_fields)
       user.set_password(password)
       user.save()
       return user

   def create_superuser(self, email, password=None, **extra_fields):
       email = self.normalize_email(email)
       user = self.model(email=email, is_superuser=True, is_staff=True, **extra_fields)
       user.set_password(password)
       user.save()
       return user
