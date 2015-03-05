from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Meme(models.Model):
    title = models.CharField(max_length=160)
    # date stamp when the object is saved
    pub_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    author = models.ForeignKey(User, blank=True, null=True)

    # To display the title of the meme when testing and checking the db
    def __str__(self):
        return self.title


class Vote(models.Model):
    winner = models.ForeignKey(Meme, related_name='winner', null=True)
    loser = models.ForeignKey(Meme, related_name='loser', null=True)
    user_id = models.ForeignKey(User, null=True, blank=True)
    date_voted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    not_scored = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' % (self.winner, self.loser)


class Score(models.Model):
    score = models.IntegerField()
    meme_id = models.ForeignKey(Meme)
    # iteration might be implemented if multiple scoring algorithms are used
    # iteration = models.IntegerField()

    # class Meta:
    #     unique_together = (("meme_id", "iteration"))

    def __str__(self):
        return '%s %s' % (self.meme_id.title, self.score)

    # def set_default_score(self, meme_id):
    #     default_score = 0
    #     try:
    #         Score.objects.get(meme_id=meme_id).update(score=default_score)
    #     except ObjectDoesNotExist:
    #         Score.objects.create(score=default_score, meme_id=meme_id)

    # def new_score(self, meme_object):
    #     # get id of meme
    #     get_id = meme_object.id
    #     wins = get_winner_votes(get_id).count()
    #     losses = get_loser_votes(get_id).count()
    #     return wins - losses

    # def get_winner_votes(winner):
    #     vote_winner_list = Vote.objects.filter(winner_id=winner)
    #     return vote_winner_list

    # def get_loser_votes(loser):
    #     vote_loser_list = Vote.objects.filter(loser_id=loser)
    #     return vote_loser_list

    # def winning_percent(meme_object_id):
    #     wins = get_winner_votes(meme_object_id).count()
    #     losses = get_loser_votes(meme_object_id).count()
    #     total_votes = wins + losses
    #     if total_votes == 0:
    #         default_percent = 50
    #         return default_percent
    #     else:
    #         temp = wins / total_votes * 100
    #         rounding = round(temp, 1)
    #         return rounding

    # def score_list():
    #     winners = []
    #     memes = Meme.objects.all()
    #     for m in memes:
    #         new = new_score(m)
    #         winners.append(new)
    #         print(winners)
    #     return winners

    # def percent_list():
    #     percents = []
    #     memes = Meme.objects.all()
    #     for m in memes:
    #         new = winning_odds(m.id)
    #         percents.append(new)
    #     return percents
