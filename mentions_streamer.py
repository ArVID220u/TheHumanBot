# the MentionsStreamer is a subclass of TwythonStreamer
from twython import TwythonStreamer
# import twythonaccess to be able to send tweets
import twythonaccess
# import setup for screen name
import setup

# the MentionsStreamer class will use the streaming api to check for new tweets.
# It will be used for filtering all tweets containing a mention of self.
# This class could technically be used to reply to all kinds of tweets.
class MentionsStreamer(TwythonStreamer):

    # this function will be called when a tweet is received
    def on_success(self, tweet):

        # Filter out all retweets of the replies
        if tweet["text"].startswith("RT"):
            return
        if "retweeted_status" in tweet:
            return

        print("reply!")

        # do not reply to self — it will cause an endless loop
        if tweet["user"]["screen_name"] == setup.TWITTER_USERNAME:
            print("from self; no reply will be sent")
            return

        # reply with the standard reply
        reply = "@" + tweet["user"]["screen_name"] + " " + setup.STANDARD_REPLY
        print("will send in reply in 10 s: " + reply)
        time.sleep(10)
        twythonaccess.send_tweet(tweet = reply, twitter_app = twythonaccess.TwitterApp.mentions, in_reply_to_status_id = tweet["id"])
        return


    # when an error is caught
    def on_error(self, status_code, data):
        print("STREAMING API ERROR IN MENTIONSSTREAMER!")
        print("Status code:")
        print(status_code)
        print("Other data:")
        print(data)
        print("END OF ERROR MESSAGE")
