from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from tastypie.test import ResourceTestCase
from chilies.views import home


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)


class UserApiTest(ResourceTestCase):
    """Tests for the /user/ API endpoint."""

    fixtures = ['users.json']

    def setup(self):
        """Set up basic view client."""
        super(UserApiTest, self).setup()

    def test_user_get_api_json(self):
        """Assert that user API is displayed as a json dictionary."""
        resp = self.api_client.get('/api/v1/user/', format='json')
        self.assertValidJSONResponse(resp)

    def test_user_list_has_objects(self):
        """Assert that user json has 3 user objects."""
        resp = self.api_client.get('/api/v1/user/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 3)

    def test_user_get_expected_data(self):
        """
        Assert that an user object displays data for email, first_name,
        last_name, username, id, and resource_uri.
        """
        resp = self.api_client.get('/api/v1/user/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'email': 'dvgbiogeek@gmail.com',
            'first_name': '',
            'id': 1,
            'last_name': '',
            'resource_uri': '/api/v1/user/1/',
            'username': 'danielleglick'
        })


class MemeApiTest(ResourceTestCase):
    """Tests for the /meme/ API endpoint."""

    fixtures = ['memes.json', 'users.json']

    def setup(self):
        """Set up basic view client."""
        super(MemeApiTest, self).setup()

    def test_user_get_api_json(self):
        """Assert that meme API is displayed as a json dictionary."""
        resp = self.api_client.get('/api/v1/meme/', format='json')
        self.assertValidJSONResponse(resp)

    def test_user_list_has_objects(self):
        """Assert that meme json has 5 meme objects."""
        resp = self.api_client.get('/api/v1/meme/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 5)

    def test_user_get_expected_data(self):
        """
        Assert that a meme object displays data for image_url, title, pub_date,
        user, id, and resource_uri.
        """
        resp = self.api_client.get('/api/v1/meme/')
        self.assertEqual(self.deserialize(resp)['objects'][4], {
            'id': 46,
            'image_url': 'https://farm8.staticflickr.com/7496/15603633928_a7d6b65aeb_b.jpg',
            'pub_date': '2015-02-20T06:32:34.834000',
            'resource_uri': '/api/v1/meme/46/',
            'title': 'city at night',
            'user': 'danielleglick'
        })


class VoteApiTest(ResourceTestCase):
    """Tests for the /vote/ API endpoint."""

    fixtures = ['memes.json', 'users.json', 'vote.json']

    def setup(self):
        """Set up basic view client."""
        super(VoteApiTest, self).setup()

    def test_user_get_api_json(self):
        """Assert that vote API is displayed as a json dictionary."""
        resp = self.api_client.get('/api/v1/vote/', format='json')
        self.assertValidJSONResponse(resp)

    def test_user_list_has_objects(self):
        """Assert that vote json has 6 vote objects."""
        resp = self.api_client.get('/api/v1/vote/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 6)

    def test_user_get_expected_data(self):
        """
        Assert that a vote object displays data for winner, loser, voter,
        username, id, and resource_uri.
        """
        resp = self.api_client.get('/api/v1/vote/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': 244,
            'date_voted': '2015-02-20T06:33:10.759000',
            'loser': 'Mine!',
            'loser_id': 43,
            'not_scored': False,
            'resource_uri': '/api/v1/vote/244/',
            'user': None,
            'voter_id': 1,
            'voter_name': 'danielleglick',
            'winner': 'Made it!',
            'winner_id': 44
        })


class ScoreApiTest(ResourceTestCase):
    """Tests for the /score/ API endpoint."""

    fixtures = ['memes.json', 'score.json', 'users.json']

    def setup(self):
        """Set up basic view client."""
        super(ScoreApiTest, self).setup()

    def test_user_get_api_json(self):
        """Assert that score API is displayed as a json dictionary."""
        resp = self.api_client.get('/api/v1/score/', format='json')
        self.assertValidJSONResponse(resp)

    def test_user_list_has_objects(self):
        """Assert that score json has 4 score objects."""
        resp = self.api_client.get('/api/v1/score/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 4)

    def test_user_get_expected_data(self):
        """
        Assert that a score object displays data for meme, score, id, and
        resource_uri.
        """
        resp = self.api_client.get('/api/v1/score/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': 19,
            'meme': 'Mine!',
            'resource_uri': '/api/v1/score/19/',
            'score': 10,
        })
