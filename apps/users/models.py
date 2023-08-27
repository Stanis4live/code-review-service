from django.db import models
from django.contrib.auth.models import User

class CodeFile(models.Model):
    # Внешний ключ, on_delete=models.CASCADE: при удалении пользователя все связанные с ним файлы также будут удалены,
    # related_name='files': позволяет обращаться к связанным файлам через атрибут files у объекта пользователя,
    # например, используя some_user.files.all().
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    # Позволит загружать файлы, указывает папку, куда будут загружаться файлы (относительно настройки MEDIA_ROOT).
    file = models.FileField(upload_to='code_files/')
    # Хранить дату и время загрузки файла, автоматически устанавливает текущую дату и время при создании новой записи.
    uploaded_at = models.DateTimeField(auto_now_add=True)
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
