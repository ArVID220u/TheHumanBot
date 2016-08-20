# import the twython module
import twythonaccess
# import time and sys
import time
# import Thread to be able to run concurrently
from threading import Thread
# randint for the tweet interval
from random import randint
# import the streamers
from tweet_streamer import TweetStreamer
from mentions_streamer import MentionsStreamer
# import the coordinator
from coordinator import Coordinator
# import setup to get search phrase and api keys
import setup
# import the similarity analyzer
from similarity_analyzer import SimilarityAnalyzer
# import the send error message function
from error_messenger import send_error_message

# the main function will be called when this script is called in terminal
# the bash command "python3 mainbot.py" will call this function
def main():
    while True:
        try:
            # declare the global coordinator, and initialize
            global coordinator
            coordinator = Coordinator()
            print("initialized coordinator ")
            # Initialize the similarity analyzer, and add it to the coordinator
            global similarity_analyzer
            similarity_analyzer = SimilarityAnalyzer()
            coordinator.similarity_analyzer = SimilarityAnalyzer()
            break
        except Exception as exception:
            print("Error in setup")
            print(exception)
            send_error_message(exception, "main")
            print("will sleep for 2 hours to try to solve the problem, though time will probably not solve it by itself")
            time.sleep(2 * 60 * 60)
            print("has slept in setup error. will start anew")
    # create five threads. they are loops, complete with error handling, that all will continue running indefinitely
    # the two streamers
    tweet_streamer_thread = Thread(target = run_tweet_streamer)
    mentions_streamer_thread = Thread(target = run_mentions_streamer)
    # the three coordinator threads
    # they each interact by using common lists, but they never call each other
    # thus, they interact with each other, but never interfere with each other
    similarity_analysis_thread = Thread(target = coordinator.similarity_analysis_loop)
    send_tweet_thread = Thread(target = coordinator.send_tweet_loop)
    response_checker_thread = Thread(target = coordinator.response_checker_loop)
    # The export data loop should ensure data is backed up (at possibly future server and at disk)
    export_data_thread = Thread(target = similarity_analyzer.export_data_loop)
    # start the six loops simultaneously
    tweet_streamer_thread.start()
    similarity_analysis_thread.start()
    send_tweet_thread.start()
    response_checker_thread.start()
    export_data_thread.start()
    # only start the mentions streamer if there is a standard reply
    if setup.STANDARD_REPLY != None:
        mentions_streamer_thread.start()


# this function will create the abusive_streamer, and start its filtering based on the trigger word
def run_tweet_streamer():
    # error handling
    while True:
        try:
            # initialize the streamer with the main api keys
            streamer = TweetStreamer(setup.MAIN_CONSUMER_KEY, setup.MAIN_CONSUMER_SECRET, setup.MAIN_ACCESS_TOKEN, setup.MAIN_ACCESS_TOKEN_SECRET)
            # pass the coordinator instance to the streamer
            streamer.coordinator = coordinator
            # start the filtering
            print("starting abusive streaming")
            streamer.statuses.filter(track=setup.SEARCH_PHRASE, language=setup.LANGUAGE)
        except Exception as exception:
            # print the exception and then sleep for 2 hours
            # the sleep will reset all rate limiting
            print(exception)
            send_error_message(exception, "run_tweet_streamer")
            print("will sleep for 2 hours two avoid exception in tweet streamer")
            time.sleep(2 * 60 * 60)
            print("finished sleep after exception in tweet streamer. will now start anew")
            


# this function initializes and runs the mentions_streamer
def run_mentions_streamer():
    # initialize it with the apikeys for the mentions application
    # error handling
    while True:
        try:
            # start the filtering
            streamer = MentionsStreamer(setup.MENTIONS_CONSUMER_KEY, setup.MENTIONS_CONSUMER_SECRET, setup.MENTIONS_ACCESS_TOKEN, setup.MENTIONS_ACCESS_TOKEN_SECRET)
            print("starting mentions streaming")
            streamer.statuses.filter(track = ("@" + setup.TWITTER_USERNAME))
        except Exception as exception:
            # print the exception and then sleep for two days
            # the sleep will reset all rate limiting
            print(exception)
            send_error_message(exception, "run_mentions_streamer")
            print("will sleep for 2 hours to avoid exception in mentions streamer")
            time.sleep(2 * 60 * 60)
            print("finished sleep after exception in mentions streamer. will now start anew")


# if called directly (as in "python3 mainbot.py"), then call main() function
if __name__ == "__main__":
        main()
