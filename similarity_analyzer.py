# import time for the export data loop
import time



# The similarity analyzer class
# It needs to be a class, since it needs to have an initialization
class SimilarityAnalyzer():
    


    # On init, load the frequnecy dictionary file into a native dictionary
    # This is to reduce access time from linear to constant
    def __init__(self):
        print("initializing the similarity analyzer")








    # The export data loop is run in its own thread, indefinitely
    # Every hour, it writes the frequency dictionary to disk
    # In future implementations, and if humanbot grows big, it also uploads
    # the response data and the frequency data to the server
    def export_data_loop(self):
        while True:
            # Sleep for an hour
            time.sleep(60 * 60)
            # Export the data
            print("exporting data, figuratively")
