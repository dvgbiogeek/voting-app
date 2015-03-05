from scorer import scorers
from chilies.models import Vote, Score, Meme


def rescore_all_games(scorer):
    """Takes scorer of the type scorer = scorers.VoteScorer()"""
    # Reset scores to default
    # First retrive all scores, get their meme_id, then update each score to
    # the scoring default
    scores = Score.objects.all()
    for score in scores:
        get_meme_id = score.meme_id
        Score.objects.filter(meme_id=get_meme_id).update(
                score=scorer.initial_score)
    # Collect all the votes
    votes = Vote.objects.all()
    # Score the votes in order.
    for vote in votes:
        # First update the not_scored attribute to False
        if vote.not_scored:
            Vote.objects.filter(pk=vote.id).update(not_scored=False)
        # Score the game, and load to the database.
        scorers.record_new_scores(vote, scorer)


scorer = scorers.VoteScorer()
# rescore_all_games(scorer)
