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
# Same capitalization as on Twitter is important
TWITTER_USERNAME = "screen name"

# This is a boolean value, that deeply affects the bot's persona
# If true: the criterion for getting added to the database, is that the response should
#          be liked (favorited) by the respondee, i.e. the writer of the original tweet
# If false: the response with the most likes and retweets (combined), will get added to the database
# The true one creates a bot that will act more like the tweeter's best friend
# That is, more supportive, generally more kind, and never offensive
# If false, the bot will generally be more witty, and may be questioning
# the original tweeter, sometimes in an offensive way
FAVOR_RESPONSES_LIKED_BY_THE_RESPONDEE = True

# The reply to send to users @-mentioning the bot
# At the moment, this is not dynamic, but maybe it should be?
# If the bot should not reply to users @-mentioning it, set this preference to None,
# and do not bother adding api keys for the mentions app
STANDARD_REPLY = "standard reply"

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

# A string indicating the screen name of a twitter user who should receive error messages via DM (again, screen name without '@')
# Set this to None to not send error messages to anyone, and then don't bother filling in the api keys
# Note that the recipient must either follow the bot, or have opened their DMs to all
ERROR_MESSAGE_RECIPIENT_SCREEN_NAME = None
ERROR_MESSAGE_CONSUMER_KEY = "if enabling error messaging, enter your error message twitter application consumer key"
ERROR_MESSAGE_CONSUMER_SECRET = "if enabling error messaging, enter your error message twitter application consumer secret key"
ERROR_MESSAGE_ACCESS_TOKEN = "if enabling error messaging, enter your error message twitter application access token"
ERROR_MESSAGE_ACCESS_TOKEN_SECRET = "if enabling error messaging, enter your error message twitter application secret access token"
