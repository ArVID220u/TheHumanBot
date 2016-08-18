# The search phrase
# The bot will only interact with tweets containing this search phrase
# The search phrase also affects the responses database;
# a response will only be added to the database if its base tweet contains the search phrase
# Altogether, this means that the search phrase deeply defines the nature, the persona, of the bot
# Note: the search phrase should be formatted according to Twitter guidelines,
# e.g. with space for AND search and comma for OR search
# Don't make the search phrase too broad (e.g. by using OR search),
# since Twitter will limit the number of tweets sent to the bot, if needed
SEARCH_PHRASE = "search phrase"

# The language this bot is set on
# Multiple languages can be defined, with a comma separated list
# However, this is not recommended
# The language codes are defined in the Twitter API spec
LANGUAGE = "en"

# The username of the bot, on Twitter
# Do not include an @ sign
TWITTER_USERNAME = "screen name"

# The Twitter API keys needed to send tweets
# Four applications are needed, so two streamers can be run simultaneously, and api calls can be made without interference

# These keys are for the main streamer (read access)
MAIN_CONSUMER_KEY = "enter your main twitter application consumer key"
MAIN_CONSUMER_SECRET = "enter your main twitter application consumer secret key"
MAIN_ACCESS_TOKEN = "enter your main twitter application access token"
MAIN_ACCESS_TOKEN_SECRET = "enter your main twitter application secret access token"

# These keys are for sending the tweets (write access)
SEND_TWEET_CONSUMER_KEY = "enter your send tweet twitter application consumer key"
SEND_TWEET_CONSUMER_SECRET = "enter your send tweet twitter application consumer secret key"
SEND_TWEET_ACCESS_TOKEN = "enter your send tweet twitter application access token"
SEND_TWEET_ACCESS_TOKEN_SECRET = "enter your send tweet twitter application secret access token"

# These keys are for searching for the best responses
RESPONSE_CHECKER_CONSUMER_KEY = "enter your response checker twitter application consumer key"
RESPONSE_CHECKER_CONSUMER_SECRET = "enter your response checker twitter application consumer secret key"
RESPONSE_CHECKER_ACCESS_TOKEN = "enter your response checker twitter application access token"
RESPONSE_CHECKER_ACCESS_TOKEN_SECRET = "enter your response checker twitter application secret access token"

# These are the access keys for the mentions streamer (read and write access)
MENTIONS_CONSUMER_KEY = "enter your mentions twitter application consumer key"
MENTIONS_CONSUMER_SECRET = "enter your mentions twitter application consumer secret key"
MENTIONS_ACCESS_TOKEN = "enter your mentions twitter application access token"
MENTIONS_ACCESS_TOKEN_SECRET = "enter your mentions twitter application secret access token"
