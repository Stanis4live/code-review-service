from django import forms
from .models import CodeFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CodeFile
        fields = ['file']
