from django.db import models
from .enums import name_profession


# Create your models here.
class Name(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(
        upload_to="thumbnails/", height_field=None, width_field=None, max_length=None
    )
    profession = models.CharField(
        null=True, blank=True, choices=name_profession, max_length=50
    )

    def __str__(self):
        return self.name
