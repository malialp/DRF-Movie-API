from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils import random_id
from PIL import Image

def get_deleted_user_instance():
	return User.objects.get(username="DELETED-USER")

def image_size_validator(image):
	file_size = image.file.size
	max_size = 10.0
	if file_size > max_size * 1024 * 1024:
		raise ValidationError('You cannot upload file more than 10Mb')
	return image


class Director(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id)
	name = models.CharField(max_length=250)
	birthdate = models.DateField()

	def __str__(self):
		return self.name

class Movie(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id)
	title = models.CharField(max_length=250, unique=True)
	director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")
	duration = models.TimeField()
	release_date = models.DateField()
	imdb_rating = models.DecimalField(max_digits=2, decimal_places=1)


	def __str__(self):
		return f"{self.title} - {self.director}"
	

class Review(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id)
	author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance), related_name='reviews')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
	user_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	content = models.TextField(max_length=512)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.author} - {self.content[:50]}'
	

class MovieList(models.Model):
	id = models.CharField(primary_key=True, max_length=11, unique=True, editable=False, default=random_id)
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True, default='')
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
	movies = models.ManyToManyField(Movie, related_name='movies', blank=True)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'MovieList'
		verbose_name_plural = 'MovieLists'

	def __str__(self):
		return self.title


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	pic = models.ImageField(upload_to='images/', blank=True, null=True)
	bio = models.TextField(max_length=256, blank=True, null=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.pic:
			img = Image.open(self.pic.path)
			if img.height > 1080 or img.width > 1080:
				output_size = (1080,1080)
				img.thumbnail(output_size)
				img.save(self.pic.path)

	def __str__(self):
		return f"{self.user.username}'s Profile"

class WatchList(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='watchlist')
	movies = models.ManyToManyField(Movie, related_name='watchlists', blank=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username}'s WatchList"