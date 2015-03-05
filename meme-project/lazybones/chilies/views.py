from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from random import randrange
import json

from chilies.models import Meme, Score
from scorer import scorers


def home(request):
    return render(request, 'home.html')


def meme_display(request):
    """
    Scores the last vote and then displays memes from the db at /chilies/test.
    """
    scorer = scorers.VoteScorer()
    try:
        scorers.score_last_vote(scorer)
    except DoesNotExist:
        print("exception with scoring in meme display")
    memes = get_random_memes()
    return HttpResponse(memes)


def get_random_memes():
    """
    Retrives 2 memes from the db at random and returns as json dictionary.
    """
    num_results = 2
    result = []
    tried_index = []
    # first determine the highest pk value of the Memes in the database
    max_pk = Meme.objects.order_by('pk').reverse()[0].pk
    # while less than 2 results are in the list and the number of tried values
    # is less than the max pk value add memes to the list
    while len(result) < num_results and len(tried_index) < max_pk:
        rand_pk = randrange(1, max_pk + 1)
        if rand_pk in tried_index:
            continue
        else:
            tried_index.append(rand_pk)
        try:
            new_result = Meme.objects.get(pk=rand_pk)
            result.append(new_result)
        except ObjectDoesNotExist:
            continue
    meme_obs = meme_dict_from_object(result)
    return json.dumps(meme_obs)


def meme_dict_from_object(result):
    """
    Takes a list of meme objects and generates a dictionary of selected memes.
    """
    meme_list = []
    for e in result:
        try:
            score = Score.objects.get(meme_id=e).score
        except ObjectDoesNotExist:
            score = scorer.initial_score
        meme_dict = {
            "id": e.id,
            "title": e.title,
            "image_url": e.image_url,
            "score": score
        }
        meme_list.append(meme_dict)
    return meme_list
