import random
from chilies.models import Meme, Vote, Score
from django.core.exceptions import ObjectDoesNotExist


class Scorer(object):
    """Stub class for scorers.

    All scorers must have initial_score and score_game.
    """
    def __init__(self):
        self.initial_score = None

    def score_game(self):
        pass


class VoteScorer(Scorer):
    """Base Class for Scoring games."""

    def __init__(self):
        # Initialize Board.
        self.initial_score = 0

    def score_game(self, winner, loser):
        """Take winner and loser objects and score the game.

        Objects must have a 'score' property.
        """
        # Takes a winner and adds 1, for the loser subtracts 1
        new_winner_score = winner.score + 1
        new_loser_score = loser.score - 1

        return new_winner_score, new_loser_score


class PattiScorer(Scorer):
    """Base class for messing with patti."""

    def __init__(self, min_range=0, max_range=10):
        # Initialize Board.
        self.min_range = min_range
        self.max_range = max_range
        self.initial_score = random.randrange(min_range, max_range)

    def score_game(self, winner, loser):
        """Take winner and loser objects and score the game.

        Objects must have a 'score' property.
        """
        # score is random for winner and loser
        new_winner_score = random.randrange(min_range, max_range)
        new_loser_score = random.randrange(min_range, max_range)

        return new_winner_score, new_loser_score


def load_meme_score(meme_object, scorer):
    """Load a meme score by primary key

    Creates score record if needed in db.
    """
    # an instance of the scorer class needs to be instanciated prior to running
    # function - ex. s = scorers.VoteScorer()
    try:
        # load score if in the database
        score = Score.objects.get(meme_id=meme_object)
    except ObjectDoesNotExist:
        # if not in the database, create score with initial default
        # print('Score object not in database, adding score')
        score = Score.objects.create(meme_id=meme_object,
                score=scorer.initial_score)
        # print(score)
        # raise("There was a database error.")
    return score


def record_new_scores(vote, scorer):
    """Score a game, and record it to the database."""
    current_winner_score = load_meme_score(vote.winner, scorer)
    current_loser_score = load_meme_score(vote.loser, scorer)
    # Calculate the new scores.
    new_winner_score, new_loser_score = scorer.score_game(current_winner_score,
            current_loser_score)
    # Update scores in database.
    score_winner = Score.objects.filter(meme_id=vote.winner).update(
            score=new_winner_score)
    score_loser = Score.objects.filter(meme_id=vote.loser).update(
            score=new_loser_score)


def score_last_vote(scorer):
    """Scores the last vote entered into the database."""
    vote = Vote.objects.last()
    # If the vote has not yet been scored, update to not_scored attribute to
    # False and then score the vote
    if vote.not_scored:
        Vote.objects.filter(pk=vote.id).update(not_scored=False)
        record_new_scores(vote, scorer)
    else:
        pass
