from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#System work with a admins of a organization and normaluser

#Rewrite manager of the users
class MyUserManager(BaseUserManager):

     def create_user(self, username, password=None):
         if not username:
             raise ValueError('Es necesario tener un nombre de usuario')
         user = self.model(username=username,)
         user.set_password(password)
         user.save(using=self._db)
         return user

     def create_superuser(self, username, password):
         user = self.create_user(username,password=password,)
         user.is_admin = True
         user.save(using=self._db)
         return user

# Temporal model, it must have their own app
class Org(models.Model):
    username = models.CharField(verbose_name = 'Nombre de la organizacion', max_length = 50, unique = True)

#A normal user has email, username
class AbstractSystemUser(AbstractBaseUser):

     email = models.EmailField(verbose_name='email', max_length=255, unique=True, blank=True, null=True)
     username = models.CharField(verbose_name = 'Nombre de usuario', max_length = 50, unique = True)
     org = models.ForeignKey(Org, verbose_name = 'Manager', null=True, blank = True, on_delete=models.CASCADE)
     created = models.DateTimeField(verbose_name = 'Creado', editable = False, auto_now_add = True)
     modified = models.DateTimeField(verbose_name = 'Actualizado', editable = False, auto_now = True)
     is_active = models.BooleanField(verbose_name = 'Activo',default=True)
     is_admin = models.BooleanField(verbose_name = 'Administrador', default=False)

     objects = MyUserManager()
     USERNAME_FIELD = 'username'
     REQUIRED_FIELDS = []


     class Meta:
         verbose_name        = 'User'
         verbose_name_plural = 'Users'
         abstract            = True


     @property
     def is_superuser(self):
         return self.is_admin


     @property
     def is_staff(self):
         return self.is_admin


class NormalUser(AbstractSystemUser):
    pass


#Manager of the organization, has reference
class ManagerUser(AbstractSystemUser):

     is_active = models.BooleanField(verbose_name = 'Activo',default=True)
     is_admin = models.BooleanField(verbose_name = 'Administrador', default=True)


     class Meta:
         verbose_name        = 'Manager'
         verbose_name_plural = 'Managers'


     def __str__(self):
         return "%s(%s)" % (self.org_name ,self.user)
