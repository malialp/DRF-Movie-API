from django.urls import path
from core.api import views

urlpatterns = [
	path('movies/', views.MovieAPIView.as_view(), name='movies'),
	path('movies/<str:pk>/', views.MovieDetailAPIView.as_view(), name='movie-detail'),
	path('movies/<str:pk>/reviews/', views.ReviewCreateAPIView.as_view(), name='movie-reviews'),
	path('directors/', views.DirectorAPIView.as_view(), name='directors'),
	path('directors/<str:pk>/', views.DirectorDetailAPIView.as_view(), name='director-detail'),
    path('reviews/<str:pk>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),
    path('movielists/', views.MovieListAPIView.as_view(), name='movielists'),
    path('movielists/<str:pk>/', views.MovieListDetailAPIView.as_view(), name='movielist-detail'),
    path('profile/<str:pk>/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/<str:pk>/likes/', views.ProfileLikeAPIView.as_view(), name='likes'),
]