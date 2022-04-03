from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.core import validators
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):

        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.is_staff= True
        user.save()

        return user
        
    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(
            password= password,
            username= username,
        )
        user.is_staff= True
        user.is_superuser= True
        user.save(using= self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'), max_length=30, unique=True, blank=True, null=True,
        help_text=_('30 characters or fewer. Letters, digits and _ only.'),
        validators=[
            validators.RegexValidator(
                r'^\w+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers and _ character.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("The username is already taken."),
        }
    )
    email = models.EmailField(max_length=255, unique=True)
    last_login_date = models.DateTimeField(auto_now=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(_('staff status'),default=False)
    USERNAME_FIELD = 'username'

    objects = UserAccountManager()

    def __str__(self):
        return str(self.username)

    class Meta(object):
        verbose_name = _('Seller')
        verbose_name_plural = _('Sellers')
        abstract = False
        db_table = 'auth_user'

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        print(type(self.password))
        super(Users, self).save(*args, **kwargs)

        
        