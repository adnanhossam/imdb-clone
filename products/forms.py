from django import forms

from cast.models import Name
from .models import Products
from .enums import product_types


class ProductForm(forms.ModelForm):
    director = forms.ModelChoiceField(Name.objects.all())
    writer = forms.ModelChoiceField(Name.objects.all())
    actors = forms.ModelChoiceField(Name.objects.all())
    year_of_production = forms.IntegerField(widget=forms.NumberInput())
    length = forms.IntegerField(widget=forms.NumberInput())
    imdb_rating = forms.FloatField(widget=forms.NumberInput())
    your_rating = forms.FloatField(widget=forms.NumberInput())
    type = forms.ChoiceField(choices=product_types, initial="")

    class Meta:
        model = Products
        fields = [
            "name",
            "director",
            "writer",
            "actors",
            "year_of_production",
            "length",
            "imdb_rating",
            "your_rating",
            "thumbnail",
            "type",
        ]

    def clean_year_of_production(self):
        value = self.cleaned_data["year_of_production"]
        if not isinstance(value, int):
            raise forms.ValidationError("Enter a whole number")
        return value

    def clean_length(self):
        value = self.cleaned_data["length"]
        if not isinstance(value, int):
            raise forms.ValidationError("Enter a whole number")
        return value

    def clean_writer(self):
        writer_input = self.data["writer"]

        # If input is a string (not an instance), attempt to fetch the Writer object
        writer = Name.objects.filter(id=writer_input)
        if not writer.exists():
            raise forms.ValidationError(f"Writer '{writer_input}' does not exist.")

        return writer

    def clean_director(self):
        director_input = self.data["director"]

        # If input is a string (not an instance), attempt to fetch the Writer object
        try:
            director = Name.objects.get(id=director_input)
        except Name.DoesNotExist:
            raise forms.ValidationError(f"Director '{director_input}' does not exist.")

        return director

    def clean_actors(self):
        actors_input = self.data["actors"]

        # If input is a string (not an instance), attempt to fetch the Writer object
        actor = Name.objects.filter(id=actors_input)
        if not actor.exists():
            raise forms.ValidationError(f"Director '{actors_input}' does not exist.")

        return actor

    def clean_imdb_rating(self):
        value = self.cleaned_data["imdb_rating"]
        if not isinstance(value, float):
            raise forms.ValidationError("Enter a number")
        return value

    def clean_your_rating(self):
        value = self.cleaned_data["your_rating"]
        if not isinstance(value, float):
            raise forms.ValidationError("Enter a number")
        return value

    def clean(self):
        cleaned_data = super().clean()  # Get the basic cleaned data first

        try:
            actor = self.clean_actors()
            director = self.clean_director()
            writer = self.clean_writer()

            cleaned_data["actors"] = actor
            cleaned_data["director"] = director
            cleaned_data["writer"] = writer

            if not all([actor, director, writer]):
                raise forms.ValidationError("Missing required cast information")

        except forms.ValidationError as e:
            raise e

        return cleaned_data
