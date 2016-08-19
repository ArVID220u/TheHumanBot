# import the similarity analyzer class
from similarity_analyzer import SimilarityAnalyzer
# import datetime for the timestamp in response checked queue
from datetime import datetime, timedelta
# import time to be able to sleep
import time
# import twythonaccess to be able to send tweets
import twythonaccess
# import setup to be able to read the persona
import setup





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



    # The queue of tweets to be sent
    # This should be kept under, say, 100 elements
    # This is to ensure the response isn't all too delayed, but still somewhat delayed
    # The data is a tuple, on the following form: (reply_text, base_tweet)
    send_tweet_queue = []



    # The queue of tweets to be response checked
    # It takes around 1 minute to process each tweet
    # And a waiting time of around 5 hours should be suitable
    # Thus, the limit to this queue should be 300 elements
    # The elements are constituted by a tuple: (timestamp, tweet)
    # They should not be processed if less than 2 hours have passed
    response_checker_queue = []



    # The threshold for sending a tweet should initially be set to 0.5
    # The threshold is increased whenever a match is made, and vice versa
    # Thus, the bot will only get more accurate over time
    similarity_threshold = 0.5



    # Getting new tweets from streamer
    # Just add them to the similarity queue, after filtering out some tweets
    def new_tweet(self, tweet):
        # filter out retweets
        if tweet["text"].startswith("RT"):
            return
        if "retweeted_status" in tweet:
            return
        # don't reply to replies – they have too much context going on
        if tweet["in_reply_to_status_id"] != None:
            return
        # if the user is protected, then return
        if tweet["user"]["protected"]:
            return
        # filter out tweets containing urls – once again, we don't really know what's going on
        if tweet["entities"]["urls"]:
            return
        # add to the similarity analyzer queue, if its length is less than 100 elements
        if len(self.similarity_analyzer_queue) < 100:
            self.similarity_analyzer_queue.append(tweet)



    # This loop is run in its own thread, indefinitely
    # It takes the first element from the queue, analyzes it,
    # and appends to both the send tweet list and the response checker list
    def similarity_analysis_loop(self):
        # add error handling
        while True:
            try:
                # sleep for periods of 10 seconds until there is a tweet in the queue
                while len(self.similarity_analyzer_queue) == 0:
                    time.sleep(10)
                # Take the first element from the similarity analyzer queue
                tweet = self.similarity_analyzer_queue.pop(0)
                # analyze the tweet
                # the analyzer will return the best match tweet text, along with the similarity ratio between the tweet and its match
                # the max length of the response text has to be 140 - 1 - length of screen name - 1, for the "@screen_name " prefix
                best_match_response, similarity_ratio = self.similarity_analyzer.analyze_tweet(tweet["text"], max_length = 138 - len(tweet["screen_name"]))
                # check if the similarity ratio is greater than or equal to the threshold, or not
                if similarity_ratio >= self.similarity_threshold:
                    # yay, we can send this tweet
                    if len(self.send_tweet_queue) < 100:
                        self.send_tweet_queue.append((best_match_response, tweet))
                    # Increase the threshold, in an effort to increase the accuracy of the tweets
                    # Increase it by 0.01 (if smaller than 0.9)
                    self.similarity_threshold = min(0.9, self.similarity_threshold + 0.01)
                else:
                    # Decrease the threshold, so as to be able to finally send some tweets
                    # Never go below 0.1
                    self.similarity_threshold = max(0.1, self.similarity_threshold - 0.01)
                # if the response checked queue has fewer than 300 elements, add this tweet, along with the current timestamp
                if len(self.response_checker_queue) < 300:
                    self.response_checker_queue.append((datetime.utcnow(), tweet))
            catch Exception as exception:
                # print the exception and then sleep for 2 hours
                # the sleep will reset all rate limiting
                print(exception)
                print("will sleep for 2 hours to avoid exception in similarity analysis loop")
                time.sleep(2 * 60 * 60)
                print("finished sleep after exception in similarity analysis loop. will now start anew")




    # This function should run in its own thread, indefinitely
    # It gets tweets from the queue, and processes them to find the best response
    # If a good enough response is found, then the response and the base tweet is appended to the responses.txt
    def response_checker_loop(self):
        while True:
            try:
                # wait until there is a tweet in the queue
                while len(self.response_checker_queue) == 0:
                    time.sleep(10)
                # take the first element
                # it is a tuple, formatted (timestamp, tweet)
                timestamp, tweet = self.response_checker_queue.pop(0)
                # sleep until two hours since the tweet was sent have passed
                time.sleep(max(0, (timestamp + timedelta(hours=2) - datetime.utcnow()).total_seconds()))
                # great
                # now, lets find the replies
                # 180 calls like this one are allowed per 15 minute window
                possible_replies = twythonaccess.authorize(twitter_app = twythonaccess.TwitterApp.response_checker).search(q = "@" + tweet["user"]["screen_name"], count = 100, result_type = "recent", since_id = tweet["id"], include_entities = False)["statuses"]
                # now go through each reply, and find real replies
                real_replies = []
                for possible_reply in possible_replies:
                    if possible_reply["in_reply_to_status_id"] == tweet["id"]:
                        # yay, we found a real reply
                        real_replies.append(possible_reply)
                if not real_replies:
                    # well, to spare any api calls, simply return prematurely here
                    # wait for 8 seconds to satisfy api limits on search
                    time.sleep(8)
                    continue
                # now that we (potentially) have the real replies, find the best one
                # initialize it with None, because we might not find a suitable reply
                best_reply = None
                if setup.FAVOR_RESPONSES_LIKED_BY_THE_RESPONDEE:
                    # just choose the first tweet that seems to be liked by the respondee
                    # first get the 200 most recently liked tweets by the respondee
                    # this api call is rate limited at once per minute
                    recently_liked = twythonaccess.authorize(twythonaccess.TwitterApp.response_checker).get_favorites(user_id = tweet["user"]["id"], count = 200, since_id = tweet["id"], include_entities = False)
                    # now, we just have to check whether any of these tweets coincide with a tweet in the real_replies
                    for real_reply in real_replies:
                        for liked in recently_liked:
                            if real_reply["id"] == liked["id"]:
                                # yay! we found a reply that was liked by the original tweet author
                                # if the user has liked many replies, we don't care about that
                                best_reply = real_reply
                                break
                        else:
                            continue
                        break
                else:
                    # determine the tweet to add based on the like and retweet count
                    best_reply_like_and_retweet_count = 0
                    for real_reply in real_replies:
                        super_count = real_reply["favorite_count"] + real_reply["retweet_count"]
                        if super_count > best_reply_like_and_retweet_count:
                            best_reply = real_reply
                            best_reply_like_and_retweet_count = super_count
                # check whether the best reply is a tweet or not
                if best_reply != None:
                    # yay, we have a decent reply!
                    reply_text = best_reply["text"]
                    base_text = tweet["text"]
                    # now, remove the mentions at the start of the reply text
                    while reply_text.startswith("@"):
                        # remove the first word
                        reply_text = reply_text.split(" ", 1)[1]
                    # encode all newlines as explcitly written newlines, so that the tweets fit on one line each
                    reply_text = reply_text.replace("\n", "\\n")
                    base_text = base_text.replace("\n", "\\n")
                    # now, append the reply text and the base text to the responses.txt file
                    # the reply text should be written first, and the base text afterwards
                    # we assume that the responses.txt file is correctly formatted (i.e. preserving the always-even-lines invariant)
                    with open("responses.txt", "a") as responses_file:
                        responses_file.write(reply_text + "\n")
                        responses_file.write(base_text + "\n")
                # now, sleep for 70 seconds (to avoid rate limiting on get_favorites)
                time.sleep(70)
            except Exception as exception:
                print("oh, some error in response checker loop")
                print(exception)
                print("will wait for 2 hours")
                time.sleep(2 * 60 * 60)
                print("has slept in response checker loop, will now start anew")


    
    # This function is run in its own thread, indefinitely
    # It takes tweets from the send_tweet_queue, and sends them
    # It waits for 1 minute between each sent tweet, in an effort not to get rate limited
    def send_tweet_loop(self):
        while True:
            try:
                # sleep until there is a tweet in the queue
                while len(self.send_tweet_queue) == 0:
                    time.sleep(10)
                # take the first element
                # it is a tuple, as defined above
                reply_text, base_tweet = self.send_tweet_queue.pop(0)
                # add @screen_name to the reply text
                reply_text = "@" + base_tweet["user"]["screen_name"] + " " + reply_text
                # send the tweet
                twythonaccess.send_tweet(reply_text, twitter_app = twythonaccess.TwitterApp.send_tweet, in_reply_to_status_id = base_tweet["id"])
                # sleep for a minute
                time.sleep(60)
            except Exception as exception:
                print("oh, some error in send tweet loop")
                print(exception)
                print("will wait for 2 hours")
                time.sleep(2 * 60 * 60)
                print("has slept in send tweet loop, will now start anew")
