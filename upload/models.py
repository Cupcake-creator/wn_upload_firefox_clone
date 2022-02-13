from django.db import models
from django.urls import reverse
from passlib.hash import pbkdf2_sha256
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Upload(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, blank=True, null=True)
    max_downloads = models.IntegerField()
    expire_date = models.DateTimeField()
    file = models.FileField(upload_to='uploadedfile/')

    def __str__(self):
        path = self.file.name
        return f"{path.split('/')[-1]}"

    def verify_password(self, raw_password):
        if self.password is not None and raw_password is not None:
            return pbkdf2_sha256.verify(raw_password, self.password)
        else:
            return True

    def get_absolute_url(self):
        return reverse("download", args=(self.id))
