from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):

    class Role(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    username = models.CharField(
        'имя пользователя', max_length=150, unique=True)
    email = models.EmailField('адрес электронной почты', unique=True,
                              db_index=True)
    role = models.CharField('права пользователя',
                            max_length=9, choices=Role.choices, default='user')
    bio = models.TextField('коротко о себе', max_length=500, blank=True)
    confirm = models.CharField('код подтверждения', max_length=200, blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        ordering = ['pk']
        verbose_name = "пользователь"

    @property
    def is_moderator(self):
        return(self.role == self.Role.moderator)

    @property
    def is_admin(self):
        return(self.role == self.Role.admin or self.is_superuser)
