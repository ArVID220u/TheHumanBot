# import the similarity analyzer class
from similarity_analyzer import SimilarityAnalyzer





# The Coordinate class will coordinate all actions (wow so much info)
# It will be concurrently accessed at four different threads
# Each of its methods will only be accessed at one thread at a time
# The communication between threads is made via the class' properties (e.g. the tweet lists)
class Coordinator():


    # The queue of tweets to be analyzed for similarity
    # This should always be kept under, say, 100 elements
    # The above measure is to ensure the waiting time for similarity analysis is short,
    # i.e. we don't want a bottle neck waiting for similarity analysis
    similarity_analyzer_queue = []



    # Initializtion
    # Should set up the similarity analyzer
    def __init__(self):
        # set self's similarity analyzer
        self.similarity_analyzer = SimilarityAnalyzer()
        print("initialized similarity analyzer")




    # Getting new tweets from streamer
    # Just add them to the similarity queue, after filtering out some tweets
    def new_tweet(tweet):
        # filter out retweets
        if tweet["text"].startswith("RT"):
            return
        if "retweeted_status" in tweet:
            return
        # don't reply to replies – they have too much context going on
        if tweet["in_reply_to_status_id"] != None:
            return
        # filter out tweets containing urls – once again, we don't really know what's going on
        if tweet["entities"]["urls"]:
            return
        print("new tweet")

