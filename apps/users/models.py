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


class CodeFile(models.Model):
    # Внешний ключ, on_delete=models.CASCADE: при удалении пользователя все связанные с ним файлы также будут удалены,
    # related_name='files': позволяет обращаться к связанным файлам через атрибут files у объекта пользователя,
    # например, используя some_user.files.all().
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')
    # Позволит загружать файлы, указывает папку, куда будут загружаться файлы (относительно настройки MEDIA_ROOT).
    file = models.FileField(upload_to='code_files/')
    # Хранить дату и время загрузки файла, автоматически устанавливает текущую дату и время при создании новой записи.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # auto_now=True означает, что при каждом сохранении (при создании или изменении) поле будет автоматически
    # обновляться текущим временем.
    updated_at = models.DateTimeField(auto_now=True)
    # Хранит текущий статус файла.
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('checked', 'Checked'),
            ('modified', 'Modified')
        ],
        default='new'
    )
    #  Хранит лог проверки файла, blank=True: указывает, что поле может быть пустым при валидации,
    # null=True: указывает, что в базе данных это поле может иметь значение NULL.
    log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"File {self.id} by {self.user.email}"