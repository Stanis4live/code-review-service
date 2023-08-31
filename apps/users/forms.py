from django import forms
from django.contrib.auth.models import User
from apps.users.models import CustomUser


# ModelForm позволяет автоматически создать форму на основе модели (в данном случае User).
class RegistrationForm(forms.ModelForm):
    # widget=forms.PasswordInput гарантирует, что ввод будет скрыт.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8, max_length=20)
    password2 = forms.CharField(label='Confirm the password', widget=forms.PasswordInput, min_length=8, max_length=20)

    class Meta:
        # Какую модель использовать
        model = CustomUser
        # Какие поля из этой модели добавить в форму
        fields = ('email',)
        labels = {
            'email': 'Email',
        }

    # Автоматически вызывается после базовой валидации этого поля.
    def clean_password2(self):
        # Извлекаем значения из cleaned_data, которое является словарём с данными, введенными пользователем и уже
        # прошедшими начальную валидацию
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        # Оба пароля присутствуют, но не совпадают.
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    # стандартный метод save модели ModelForm, commit указывает, следует ли немедленно сохранять объект в базу данных
    def save(self, commit=True):
        # Создание объекта пользователя без сохранения в базе данных
        user = super().save(commit=False)
        # Установка пароля. Хэширует пароль перед сохранением в базе данных для безопасности
        user.set_password(self.cleaned_data["password1"])
        # Объект сохраняется в базе данных
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8, max_length=20)