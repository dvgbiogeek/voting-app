from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from django.contrib.auth.models import User

from chilies.models import Meme
from chilies.resources.serializer import PrettyJSONSerializer


class MemeResource(ModelResource):
    class Meta:
        queryset = Meme.objects.all()
        resource_name = 'meme'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True

    def hydrate(self, bundle):
        if bundle.request.method == 'POST':
            try:
                user_pk = bundle.request.user.id
                bundle.data['author'] = User.objects.get(pk=user_pk)
                bundle.obj.author = bundle.data['author']
            except:
                raise
        return bundle

    def dehydrate(self, bundle):
        bundle.data['user'] = bundle.obj.author
        return bundle
