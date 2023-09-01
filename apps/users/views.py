from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
import logging

# Создаем экземпляр логгера
logger = logging.getLogger(__name__)


def registration(request):
    try:
        if request.method == "POST":
            # Создаём форму на основе POST-данных
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                # Создаваём нового пользователя в базе данных с полями, которые были введены в форму.
                form.save()
                logger.info(f'Account for {email} successfully created!')
                return redirect('home')  # TODO здесь укажите название вашего представления для авторизации
            else:
                logger.warning(f'Form validation errors: {form.errors}')
        else:
            form = RegistrationForm()

        return render(request, 'registration.html', {'form': form})

    except Exception as e:
        logger.error(f"Error during registration: {e}")
        messages.add_message(request, messages.ERROR, "show_error_modal")


def user_login(request):
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                logger.info(f"Login attempt for user: {form.cleaned_data['email']}")
                # authenticate из Django проверяет, существует ли пользователь с указанным username
                user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
                if user is not None:
                    logger.info(f"User {user.email} logged in successfully.")
                    # используем встроенную функцию login, чтобы залогинить пользователя
                    login(request, user)
                    return redirect('home')  # TODO перенаправьте на главную страницу или другое представление
                else:
                    logger.error(f"Authentication error for user: {form.cleaned_data['email']}")
                    messages.add_message(request, messages.ERROR, "Invalid email or password.", extra_tags='danger')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

    except Exception as e:
        logger.error(f"Error during login: {e}")
        messages.add_message(request, messages.ERROR, "show_error_modal")





# TODO Добавить кнопку
# Декоратор гарантирует, что только авторизованные пользователи могут выходить из системы.
@login_required
def user_logout(request):
    try:
        logger.info(f"User {request.user.email} logged out.")
        logout(request)
        return redirect('home')

    except Exception as e:
        logger.error(f"Error during logout: {e}")
        messages.add_message(request, messages.ERROR, "show_error_modal")


def home_view(request):
    return render(request, "home.html")

