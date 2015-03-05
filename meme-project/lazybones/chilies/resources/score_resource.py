from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from chilies.models import Score
from chilies.resources.serializer import PrettyJSONSerializer


class ScoreResource(ModelResource):
    class Meta:
        queryset = Score.objects.all()
        resource_name = 'score'
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['meme'] = bundle.obj.meme_id
        return bundle
