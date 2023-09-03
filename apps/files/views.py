from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import CodeFile
from django.contrib import messages


def upload_file(request):
    if request.method == 'POST':
        # request.POST содержит текстовые данные формы, а request.FILES содержит файлы, загруженные через форму.
        # Форма автоматически будет проверять, был ли загружен файл (так как единственное поле в форме —
        # это поле для файла)
        form = UploadFileForm(request.POST, request.FILES)
        # Форма проверяет, соответствует ли загруженный файл требованиям модели
        if form.is_valid():
            # Создаём новый экземпляр модели CodeFile с данными из формы
            new_file = form.save(commit=False)
            # Ассоциируем загруженный файл с текущим пользователем
            new_file.user = request.user
            new_file.save()
            # Возможно, добавить сообщение для пользователя
            return redirect('file_list') # redirect to the list of uploaded files
    else:
        form = UploadFileForm()
    # {'form': form} передаёт форму для представления, которую будем использовать в шаблоне под именем form
    return render(request, 'upload_file.html', {'form': form})


# TODO нужен ли тут статус проверки?
def file_list(request):
    files = CodeFile.objects.filter(user=request.user)
    # Создаём новое поле, которое будет содержать только имя файла
    for file in files:
        file.filename = file.file.name.split("/")[-1]
    return render(request, 'file_list.html', {'files': files})


def view_file(request, file_id):
    _file = get_object_or_404(CodeFile, id=file_id)
    return render(request, 'view_file.html', {'file': _file})


def edit_file(request, file_id):
    # Получения экземпляра файла из базы данных по его ID
    file_instance = get_object_or_404(CodeFile, id=file_id)
    if request.method == 'POST':
        # instance гарантирует, что изменения будут применены к существующему экземпляру файла, а не создан новый.
        form = UploadFileForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            form.save()
            return redirect('file_list') # or wherever you want to redirect after editing
    else:
        # instance содержит экземпляр модели CodeFile. Это сообщает форме, что она должна предзаполниться данными
        # из этого экземпляра, а не быть пустой.
        form = UploadFileForm(instance=file_instance)
    return render(request, 'edit_file.html', {'form': form})


def delete_file(request, file_id):
    file_instance = get_object_or_404(CodeFile, id=file_id)
    if request.method == 'POST':
        file_instance.delete()
        messages.success(request, 'File successfully deleted!')
        return redirect('file_list')
    messages.error(request, 'Invalid request method.')
    return redirect('file_list')