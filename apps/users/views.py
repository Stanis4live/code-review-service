from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
import logging

# Создаем экземпляр логгера
logger = logging.getLogger(__name__)


def registration(request):
    if request.method == "POST":
        # Создаём форму на основе POST-данных
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Устанавливаем значение username равным значению email
            email = form.cleaned_data.get('email')
            form.instance.username = email
            # Создаваём нового пользователя в базе данных с полями, которые были введены в форму.
            form.save()
            logger.info(f'Account for {email} successfully created!')
            return redirect('name-of-login-view')  # TODO здесь укажите название вашего представления для авторизации
        else:
            logger.warning(f'Form validation errors: {form.errors}')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # authenticate из Django проверяет, существует ли пользователь с указанным username
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                # используем встроенную функцию login, чтобы залогинить пользователя
                login(request, user)
                return redirect('home')  # TODO перенаправьте на главную страницу или другое представление
            else:
                messages.add_message(request, messages.ERROR, "Invalid email or password", extra_tags='danger')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.contrib.auth import logout


# TODO Добавить кнопку
def user_logout(request):
    logout(request)
    return redirect('home.html')


def home_view(request):
    return render(request, "home.html")