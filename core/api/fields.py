from rest_framework import serializers
from rest_framework.reverse import reverse
from core.models import MovieList

class LikeHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'movielist-detail'

    def get_url(self, obj, view_name, request, format):
        print(obj)
        url_kwargs = {
         "pk": obj.movielist.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
    
    # def get_object(self, view_name, view_args, view_kwargs):
    #     lookup_kwargs = {
    #         "pk":view_kwargs['pk']
    #     }
    #     return MovieList.objects.get(**lookup_kwargs)
