from django.db import models
from .enums import product_types


class Products(models.Model):
    name = models.CharField(max_length=50)
    director = models.ForeignKey(
        "cast.Name", on_delete=models.CASCADE, related_name="directors"
    )
    writer = models.ManyToManyField("cast.Name", related_name="writers")
    actors = models.ManyToManyField("cast.Name", related_name="actors")
    year_of_production = models.IntegerField()
    length = models.IntegerField()
    imdb_rating = models.IntegerField()
    your_rating = models.IntegerField()
    type = models.CharField(choices=product_types, null=True, blank=True, max_length=50)
    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    class Meta:
        ordering = ["name"]
