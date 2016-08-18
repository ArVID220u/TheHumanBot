# This module provides the api twython object, which is used to access the api

# import datetime
from datetime import datetime

# Import twython
from twython import Twython

# import the api keys from setup
import setup

# import enum for the different apps
# Requires python 3.4?
from enum import Enum



# an enum representing the four different apps
class TwitterApp(Enum):
    tweet_streamer = 1
    send_tweet = 2
    response_checker = 3
    mentions = 4


# Store number of requests, so that they won't exceed the rate limit
mentions_requests_since_last_sleep = 0
# time of last request is used t be able t reset the requests
# utc time is reliable
mentions_time_of_last_request = datetime.utcnow()



# the twitter_app parameter is a TwitterApp enum
# only the mentions app needs to be rate limit checked, since the others manage that themselves
def authorize(twitter_app):
    if twitter_app == TwitterApp.tweet_streamer:
        # authorize
        return Twython(setup.MAIN_CONSUMER_KEY, setup.MAIN_CONSUMER_SECRET, setup.MAIN_ACCESS_TOKEN, setup.MAIN_ACCESS_TOKEN_SECRET)
    elif twitter_app == TwitterApp.send_tweet:
        # authorize
        return Twython(setup.SEND_TWEET_CONSUMER_KEY, setup.SEND_TWEET_CONSUMER_SECRET, setup.SEND_TWEET_ACCESS_TOKEN, setup.SEND_TWEET_ACCESS_TOKEN_SECRET)
    elif twitter_app == TwitterApp.response_checker:
        # authorize
        return Twython(setup.RESPONSE_CHECKER_CONSUMER_KEY, setup.RESPONSE_CHECKER_CONSUMER_SECRET, setup.RESPONSE_CHECKER_ACCESS_TOKEN, setup.RESPONSE_CHECKER_ACCESS_TOKEN_SECRET)
    elif twitter_app == TwitterApp.mentions:
        # Increment number of requests made in mentions application
        global mentions_requests_since_last_sleep
        mentions_requests_since_last_sleep += 1
        # update the last request time
        global mentions_time_of_last_request
        mentions_time_of_last_request = datetime.utcnow()
        # authorize
        return Twython(setup.MENTIONS_CONSUMER_KEY, setup.MENTIONS_CONSUMER_SECRET, setup.MENTIONS_ACCESS_TOKEN, setup.MENTIONS_ACCESS_TOKEN_SECRET)


# this method sends a tweet, by first checking with me
def send_tweet(tweet, twitter_app, in_reply_to_status_id=0):

    if len(tweet) > 140:
        print("too long tweet, not sending it")
        return

    # if in mentions streamer, and the number of requests are too large,
    # then return prematurely without sending the tweet,
    # since we don't want to clog up the streaming http connection
    if twitter_app == TwitterApp.mentions:
        # first check if requests can be reset, that is, if more than 15 minutes have elapsed since last request
        check_if_requests_can_be_reset()
        if mentions_requests_are_maximum(14):
            return

    # we don't need any rate limit check on the main bot, since a 15 minute interval between tweets
    # is assured to exist by the coordinator (blah, my english is bad)

    # maybe send it in reply to another tweet
    if in_reply_to_status_id == 0:
        # standalone tweet
        authorize(twitter_app).update_status(status=tweet)
    else:
        # tweet is a reply
        authorize(twitter_app).update_status(status=tweet, in_reply_to_status_id=in_reply_to_status_id)
    print("sent tweet: " + tweet)


# This method is called every time a request is to be made on mentions streamer
# If the requests variable is over limit, then returns true, and starts a sleep (if not already ongoing)
# else, return false
def mentions_requests_are_maximum(limit):
    global mentions_requests_since_last_sleep
    global mentions_is_sleeping 
    print("Mentions requests since last sleep: " + str(mentions_requests_since_last_sleep))
    return mentions_requests_since_last_sleep >= limit

# checking whether the last request in mentions was made more than 15 minutes ago
# if so, resets the requests, so as to be able to send new tweets
def check_if_requests_can_be_reset():
    now_time = datetime.utcnow()
    global mentions_time_of_last_request
    if (now_time - mentions_time_of_last_request).total_seconds() > 15*60:
        global mentions_requests_since_last_sleep
        mentions_requests_since_last_sleep = 0
