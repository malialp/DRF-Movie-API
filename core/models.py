from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .utils import random_id, get_path, resize, image_size_validator

def get_deleted_user_instance():
	return Profile.objects.get(user__username="DELETED-USER")


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	pic = models.ImageField(upload_to=get_path, blank=True, null=True, validators=[image_size_validator])
	bio = models.TextField(max_length=256, blank=True, null=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.pic:
			img = resize(self.pic.path)
			img.save(self.pic.path)

	def __str__(self):
		return f"{self.user.username}'s Profile"


class Director(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id(11))
	name = models.CharField(max_length=250)
	birthdate = models.DateField()

	def __str__(self):
		return self.name

class Movie(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id(11))
	title = models.CharField(max_length=250, unique=True)
	director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")
	duration = models.TimeField()
	release_date = models.DateField()
	imdb_rating = models.DecimalField(max_digits=2, decimal_places=1)


	def __str__(self):
		return f"{self.title} - {self.director}"
	

class Review(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id(11))
	author = models.ForeignKey(Profile, on_delete=models.SET(get_deleted_user_instance), related_name='reviews')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
	user_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	content = models.TextField(max_length=512)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.author.user.username} - {self.content[:50]}'
	

class MovieList(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id(11))
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True, default='')
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='lists')
	movies = models.ManyToManyField(Movie, related_name='movies', blank=True)
	likes = models.ManyToManyField(Profile, related_name='likes', blank=True)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'MovieList'
		verbose_name_plural = 'MovieLists'

	def __str__(self):
		return self.title


class WatchList(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='watchlist')
	movies = models.ManyToManyField(Movie, related_name='watchlists', blank=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username}'s WatchList"