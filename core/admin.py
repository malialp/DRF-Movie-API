from django.contrib import admin
from .models import Director, Movie, Review, MovieList, Profile, Like

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(MovieList)
admin.site.register(Profile)
admin.site.register(Like)
