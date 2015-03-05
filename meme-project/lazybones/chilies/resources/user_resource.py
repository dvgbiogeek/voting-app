from tastypie.resources import ModelResource
from django.contrib.auth.models import User

from chilies.resources.serializer import PrettyJSONSerializer


class UserResource(ModelResource):
    class Meta:
        resource_name = 'user'
        queryset = User.objects.all()
        excludes = ['is_staff', 'is_superuser', 'password', 'is_active',
                    'last_login', 'date_joined']
        serializer = PrettyJSONSerializer()
