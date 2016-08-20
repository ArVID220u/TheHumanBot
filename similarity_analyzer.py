# import time for the export data loop
import time
# send error message
from error_messenger import send_error_message



# The similarity analyzer class
# It needs to be a class, since it needs to have an initialization
class SimilarityAnalyzer():
    

    # The frequency dictionary contains information on how frequent a word is
    # The dictionary contains raw frequency count
    word_frequency = {}
    
    # The max frequency is the average of the frequency of the top 10 most common words
    # It is used to make sense of the numbers in the word_frequency dictionary
    max_frequency = 1 # dummy value
    # a list of the ten biggest frequency counts, so as to know when to update the max_frequency
    ten_biggest_frequencies = [1 for x in range(10)] # dummy values




    # On init, load the frequency dictionary file into a native dictionary
    # This is to reduce access time from linear to constant
    def __init__(self):
        # The frequency data is stored in word_frequencies.txt
        # The first line contains the ten biggest frequencies, space separated
        # The next lines contain a word followed by a space, followed by the frequency count
        with open("word_frequencies.txt") as frequency_data:
            # bool to indicate whether it is the first line or not
            first_line = True
            # iterate over each line
            for line in frequency_data:
                # remove the newline at the end
                line_string = line[:-1]
                if first_line:
                    # The first line contains the ten biggest_frequencies
                    self.ten_biggest_frequencies = [int(x) for x in line_string.split(" ")]
                    # update the max frequency to be the average
                    self.max_frequency = 0
                    for freq in self.ten_biggest_frequencies:
                        self.max_frequency += freq
                    self.max_frequency /= len(self.ten_biggest_frequencies)
                else:
                    # The first is the word, the second is the count
                    word_count_list = line_string.split(" ")
                    self.word_frequency[word_count_list[0]] = int(word_count_list[1])



    


    # Analyze the incoming tweet for similarity with any tweet in the responses data
    # Return the best match's response, along with the similarity ratio, in a tuple
    # Like, (best_match_response_text, similarity_ratio)
    # The max_length parameter defines the maximum length of the response
    def analyze_tweet(self, tweet_text, max_length):
        if tweet_text == "":
            # this should never happen, but just in case
            return ("", 0)
        # make a set of words out of the tweet_text
        base_words_set = set(tweet_text.split(" "))
        # make a list for faster enumeration
        base_words_list = list(base_words_set)
        # update the word frequencies dict
        self.update_word_frequency(tweet_text.split(" "))
        # the best response and the best similarity score will be stored here
        best_response = ""
        best_similarity_score = 0
        # open the responses data file
        # all odd rows (with indexing starting at 0) contain the base tweets, i.e. the ones to be checked against
        # all even rows contain the responses
        with open("responses.txt") as responses_file:
            # This string contains the last response, which belongs to the base tweet in the next row
            last_response = ""
            # This ticker keeps count of even or odd row
            even_or_odd_ticker = 0
            # iterate over all lines, which each contains a tweet
            # all newlines have been converted to explicitly written newlines "\\n", \n
            for line in responses_file:
                # remove the last newline character
                test_string = line[:-1]
                # remove all instances of encoded newlines, into real newlines
                test_string = test_string.replace("\\n", "\n")
                # if odd, then do similarity check
                if even_or_odd_ticker == 1:
                    even_or_odd_ticker = 0
                    # the similarity score between the base string and the test string
                    similarity_score = 0
                    # this is a tweet that should be analyzed against the base tweet
                    test_words_set = set(test_string.split(" "))
                    # iterate over each base word, and check if it is in the test words
                    for base_word in base_words_list:
                        if base_word in test_words_set:
                            # increase the similarity score by a value between 1.0 and 3.0, depending on the frequency
                            similarity_score += 1 + 2 * (1 - min(1, self.word_frequency[base_word] / self.max_frequency))
                    # iterate over each test string word, and subtract 0.05 from the similarity score for each word not in the base string
                    for test_word in test_words_set:
                        if test_word not in base_words_set:
                            similarity_score -= 0.05
                    # now we have a good similarity score between these two strings
                    # check whether it is the best, and using the most recent one if there are many with same score
                    if similarity_score >= best_similarity_score:
                        # the length of the last response has to be less than max_length
                        if len(last_response) <= max_length:
                            # yay, we can add the last response to the best response, and update the best similarity score
                            best_similarity_score = similarity_score
                            best_response = last_response
                elif even_or_odd_ticker == 0:
                    even_or_odd_ticker = 1
                    # update the last response
                    last_response = test_string
        # we now have the best response!
        # convert the score into a ratio by first calculating the max score
        max_score = 0
        for base_word in base_words_list:
            max_score += 1 + 2 * (1 - min(1, self.word_frequency[base_word] / self.max_frequency))
        # now, the similarity ratio is calculated by dividing the best match score with the max score
        # it is a standardized value between 0 and 1, with 1 indicating a full match and 0 indicating no common words
        similarity_ratio = best_similarity_score / max_score
        # now return the best match, and the ratio, as a tuple
        return (best_response, similarity_ratio)




    
    # A helper function for updating the word frequency list
    # It also updates the max frequency
    def update_word_frequency(self, words):
        for word in words:
            if word in self.word_frequency:
                self.word_frequency[word] += 1
            else:
                self.word_frequency[word] = 1
            # maybe update the max frequency
            least_frequency = self.word_frequency[word]
            least_frequency_index = 0
            for index, top10_frequency in enumerate(self.ten_biggest_frequencies):
                if top10_frequency < least_frequency:
                    least_frequency = top10_frequency
                    least_frequency_index = index
            if self.word_frequency[word] > least_frequency:
                self.ten_biggest_frequencies[least_frequency_index] = self.word_frequency[word]
                # update the max frequency
                self.max_frequency += self.word_frequency[word] / 10 - least_frequency / 10







    # The export data loop is run in its own thread, indefinitely
    # Every hour, it writes the frequency dictionary to disk
    # In future implementations, and if humanbot grows big, it also uploads
    # the response data and the frequency data to the server
    def export_data_loop(self):
        while True:
            try:
                # Sleep for an hour
                time.sleep(60 * 60)
                # Export the data
                # (1) write the word frequencies to the word_frequencies.txt
                print("writing word frequencies to disk. DON'T STOP PROGRAM EXECUTION, or else information may be lost")
                with open("word_frequencies.txt", "w") as frequency_file:
                    # first write the top 10 biggest frequnecies as the first line, joined by a space
                    frequency_file.write(" ".join(str(x) for x in self.ten_biggest_frequencies) + "\n")
                    # then, each entry in the word_frequency dict should occupy one line
                    for word, count in self.word_frequency.items():
                        frequency_file.write(word + " " + str(count) + "\n")
                print("finished writing word freuqnecies to disk. it is now (relatively) safe to halt the execution.")
            except Exception as exception:
                print(exception)
                print("Error in export_data_loop. will sleep for 2 hours")
                send_error_message(exception, "export_data_loop")
                time.sleep(2 * 60 * 60)
                print("has slept after exception in export_data_loop. will now resume")


            
