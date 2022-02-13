from django import forms
from .models import Upload
from .validater_file import validate_file
from passlib.hash import pbkdf2_sha256

from django.utils import timezone
from datetime import  timedelta

class UploadForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file])
    max_downloads = forms.ChoiceField(
        choices=[
            (1, "1 download"),
            (2, "2 downloads"),
            (3, "3 downloads"),
            (4, "4 downloads"),
            (5, "5 downloads"),
            (20, "20 downloads"),
            (50, "50 downloads"),
            (100, "100 downloads"),
        ]
    )

    expire_date = forms.ChoiceField(
        choices=[
            (5 * 60, "5 minutes"),
            (60 * 60, "1 hour"),
            (24 * 60 * 60, "1 day"),
            (7 * 24 * 60 * 60, "7 days"),
        ]
    )

    class Meta:
        model = Upload
        fields = ("password", "max_downloads", "expire_date", "file")
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        expire_date = timezone.now() + timedelta(seconds=int(expire_date))
        return expire_date

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == '' or password == None:
            return ''
        return pbkdf2_sha256.encrypt(password,rounds=12000,salt_size=32)




    
    
