from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.models import User
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
            # Проверка на уникальность email и username. Фильтрация записей модели User.
            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
                messages.error(request, f'Account with email {email} already exists.')
                logger.warning(f'Try to register already existing email: {email}')
            else:
                # Создаваём нового пользователя в базе данных с полями, которые были введены в форму.
                form.save()
                # Отправляется сообщение об успехе
                messages.success(request, f'Account for {email} successfully created! Now you can login.')
                logger.info(f'Account for {email} successfully created!')
                return redirect('name-of-login-view') # TODO здесь укажите название вашего представления для авторизации
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login():
    pass
