from rest_framework import serializers
from rest_framework.reverse import reverse

class LikeHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'movielist-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
         "pk": obj.movielist.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)