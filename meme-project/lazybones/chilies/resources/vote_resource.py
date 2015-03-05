from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from django.contrib.auth.models import User

from chilies.resources.meme_resource import MemeResource
from chilies.resources.user_resource import UserResource
from chilies.models import Vote
from chilies.models import Meme
from chilies.resources.serializer import PrettyJSONSerializer

# import pdb; pdb.set_trace()


class VoteResource(ModelResource):
    winner = fields.ForeignKey(MemeResource, 'meme', null=True, blank=True)
    loser = fields.ForeignKey(MemeResource, 'meme', null=True, blank=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True)

    class Meta:
        queryset = Vote.objects.all()
        resource_name = 'vote'
        excludes = ['user']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True
        limit = 20

    def dehydrate(self, bundle):
        """Add winner, loser, not_scored, and voter information to json dic."""
        bundle.data['winner'] = bundle.obj.winner
        bundle.data['winner_id'] = bundle.obj.winner_id
        bundle.data['loser'] = bundle.obj.loser
        bundle.data['loser_id'] = bundle.obj.loser_id
        bundle.data['not_scored'] = bundle.obj.not_scored
        if bundle.obj.user_id:
            bundle.data['voter_id'] = bundle.obj.user_id.id
            bundle.data['voter_name'] = bundle.obj.user_id.username
        else:
            bundle.data['voter_id'] = None
            bundle.data['voter_name'] = ''
        return bundle

    def hydrate(self, bundle):
        """
        Assembles the object needed for a vote
        """
        # Takes the id from winner and retrieves the object with that id
        try:
            winner_pk = bundle.data['winner']
            bundle.data['winner'] = Meme.objects.get(pk=winner_pk)
            bundle.obj.winner = bundle.data['winner']
        except chilies.models.DoesNotExist:
            # TODO: Figure out a good way to handle this.
            print('Raise an error, could not get winner id')
        # Takes the id from the loser and retrieves the object with that id
        try:
            loser_pk = bundle.data['loser']
            bundle.data['loser'] = Meme.objects.get(pk=loser_pk)
            bundle.obj.loser = bundle.data['loser']
        except chilies.models.DoesNotExist:
            print('Raise an error, could not get loser id')
        if bundle.request.method == 'POST':
            # Get the user object
            if bundle.request.user.is_authenticated():
                user_pk = bundle.request.user.id
                bundle.data['user_id'] = User.objects.get(pk=user_pk)
                bundle.obj.user_id = bundle.data['user_id']
            else:
                bundle.data['user_id'] = None
        return bundle
