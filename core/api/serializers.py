from rest_framework import serializers
from core.models import Director, Movie, Review, MovieList, Profile, Like

class MovieSerializer(serializers.ModelSerializer):
	director_id = serializers.CharField(source="director.id")

	class Meta:
		model = Movie
		exclude = ['director']

	def validate_director_id(self, value):
		director = Director.objects.filter(id=value).first()
		
		if not director:
			raise serializers.ValidationError('Director does not exist.')
		return value

	def create(self, validated_data):
		director_id = validated_data.pop('director')['id']
		
		director = Director.objects.get(id=director_id)
		movie = Movie.objects.create(director=director, **validated_data)
		
		return movie

class DirectorSerializer(serializers.ModelSerializer):
	movies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')

	class Meta:
		model = Director
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	author = serializers.StringRelatedField(read_only=True, source='author.user.username')
	movie_id = serializers.CharField(read_only=True, source='movie.id')
	
	class Meta:
		model = Review
		exclude = ['movie']


class MovieListSerializer(serializers.ModelSerializer):
	owner = serializers.StringRelatedField(read_only=True, source='owner.user.username')
	likes = serializers.IntegerField(read_only=True, source='likes.count')
	movies = MovieSerializer(many=True, read_only=True)
	
	class Meta:
		model = MovieList
		fields = '__all__'

class MovieListUpdateSerializer(MovieListSerializer):
	movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())


class LikeSerializer(serializers.ModelSerializer):
	owner = serializers.StringRelatedField(source='movielist.owner.user')
	movielist_id = serializers.StringRelatedField(source='movielist.id')
	url = serializers.HyperlinkedRelatedField(read_only=True, view_name='movielist-detail', source='movielist')

	class Meta:
		model = Like
		exclude = ['id', 'profile', 'movielist']


class ProfileSerializer(serializers.ModelSerializer):
	id = serializers.StringRelatedField(read_only=True, source='user.id')
	username = serializers.StringRelatedField(source='user.username')
	lists = MovieListSerializer(many=True, read_only=True, source='user.lists')
	reviews = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='review-detail')
	lists = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movielist-detail')
	date_joined = serializers.StringRelatedField(source='user.date_joined')
	likes = LikeSerializer(many=True, read_only=True)

	class Meta:
		model = Profile
		exclude = ['user']