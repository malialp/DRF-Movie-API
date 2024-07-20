from core.api.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, MovieListSerializer, MovieListUpdateSerializer, ProfileSerializer
from core.api.pagination import StandartMoviePagination, StandartDirectorPagination
from core.api.permissions import IsReviewAuthorOrReadOnly, IsOwnerOrReadOnly, IsUserOrReadOnly
from core.models import Movie, Director, Review, MovieList, Profile, Like

from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

class MovieAPIView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = StandartMoviePagination
    
    def get_queryset(self):
        title = self.request.query_params.get('title')
        if title:
            return Movie.objects.filter(title__icontains=title)
        else:
            return Movie.objects.all()


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class DirectorAPIView(generics.ListCreateAPIView):
    serializer_class = DirectorSerializer
    pagination_class = StandartDirectorPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return Director.objects.filter(name__icontains=name)
        else:
            return Director.objects.all()
	
    
class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

class ReviewCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        reviews = movie.reviews
        return reviews
        
    def perform_create(self, serializer):
        author = self.request.user
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])

        review = Review.objects.filter(movie=movie, author=author)

        if review.exists():
            raise ValidationError('You can only make one comment on a movie.')

        serializer.save(author=author, movie=movie)

class MovieListAPIView(generics.ListCreateAPIView):
    queryset = MovieList.objects.all()
    serializer_class = MovieListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MovieListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieList.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieListUpdateSerializer
        return MovieListSerializer

class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'user.username'
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_object(self):
        username = self.kwargs['pk']
        user = get_object_or_404(User, username__iexact=username)
        profile = Profile.objects.get(user=user)
        self.check_object_permissions(self.request, profile)
        return profile
        

class ProfileLikeAPIView(generics.views.APIView):
    http_method_names = ('post', 'delete')

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user__username__iexact=self.kwargs['pk'])
        movielist_id = request.data['id']
        movielist = MovieList.objects.filter(id=movielist_id)
        
        if not movielist.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error":{"message":"Movielist not exists."}})

        movielist = movielist.first()
        is_exists = Like.objects.filter(profile=profile, movielist=movielist).exists()

        if is_exists:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error":{"message":"Movielist already in likes."}})
        else:
            Like.objects.create(profile=profile, movielist=movielist)
            return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        movielist_id = request.data['id']
        like = Like.objects.filter(movielist__id=movielist_id)
        if like.exists():
            like.first().delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error":{"message":"Movielist not in likes."}})