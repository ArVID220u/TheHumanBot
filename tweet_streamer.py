# the TweetStreamer is a subclass of TwythonStreamer
from twython import TwythonStreamer

# the TweetStreamer class will use the streaming api to check for new tweets.
# It will be used for filtering all tweets containing the trigger word specified in setup.py
# This class could technically be used to reply to all kinds of tweets.
class TweetStreamer(TwythonStreamer):

    # this function will be called when a tweet is received
    def on_success(self, data):
        # send tweet to the coordinator, which should analyze the tweet
        self.coordinator.new_tweet(data)

    # when an error is caught
    def on_error(self, status_code, data):
        print("STREAMING API ERROR IN TWEETSTREAMER!")
        print("Status code:")
        print(status_code)
        print("Other data:")
        print(data)
        print("END OF ERROR MESSAGE")
