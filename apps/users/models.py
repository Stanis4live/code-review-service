from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Создаём свой менеджер создания пользователя на основе базового
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        # Преобразует доменную часть электронной почты в нижний регистр (метод BaseUserManager)
        email = self.normalize_email(email)
        # Создается новый пользователь с помощью переданного email и дополнительных полей
        user = self.model(email=email, **extra_fields)
        # Устанавливается пароль для пользователя. Метод set_password шифрует пароль перед сохранением
        user.set_password(password)
        # Сохраняет объект пользователя в базе данных
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    # Поле email будет использоваться в качестве идентификатора пользователя при аутентификации,
    # вместо стандартного username.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
