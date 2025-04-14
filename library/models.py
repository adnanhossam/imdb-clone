from django.db import models

# Create your models here.
# in this module we are going to create a model for movies and another for the shows
# the movies model is going to have
# 1- a name
# 2- director (should be a hyperlink)
# 3- writer (can be a list) (should be a hyperlink)
# 4-stars(list) (should be a hyperlink)
# 5- year of production (should be a hyperlink)
# 6- length
# 7- imdb rating
# 8- your rating
# 9- a picture
# relations:
#               movies---actors     manytomany
#
#               writers---movies    manytomany
#               tvshows---actors    manytomany
#
#               writers---tvshows   manytomany


# the shows module is going to be exactly the same but we'r going to add
# 1- seasons (should be a hyperlink)
# just realized we need to do a model for the actors , directors , writers


class Episodes(models.Model):
    name = models.CharField(max_length=50)


class Seasons(models.Model):
    name = models.CharField(max_length=50)
    episodes = models.ForeignKey(Episodes, on_delete=models.CASCADE)
