# -*- coding: utf-8 -*-

# This is a small app that helps make decisions (and allows me to teach myself Python)
# Beware of actually following this app's advice!

# Resources:
# Reference of parameters: https://developers.google.com/custom-search/json-api/v1/reference/cse/list
# API explorer: https://developers.google.com/apis-explorer/#p/customsearch/v1/search.cse.list?q=pizza+great&cx=013987910149588354017%253Aui0xnrn9hiw&_h=1&
# Sentinment Orientation for the Poor: https://www.linkedin.com/pulse/quick-easy-sentiment-analysis-using-google-search-result-pranab-ghosh/

# Maybe also use Twitter: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

from googleapiclient.discovery import build # Google API client
import math # Maths!
import os # use to get ENV variables

# This is a small app that helps make decisions (and allows me to teach myself Python)
# Beware of actually following this app's advice!

print("I heard you had a tough decision to make? Maybe I can help.")

####################
# Get Options      #
####################

# Get the number of options
num_options = int(input("Enter the number of options you have: "))

# Declare lists
options = []
SentimentOrientations = []

# Let's ask for the what the options are
# Remember to use range() to make an x that is iterable, and to use the append thing
for i in range(num_options):
    options.append(input("What is option number " + str(i + 1) + ": "))

# Define words that describe whether an option is good or bad
positive_attribute = "great"
negative_attribute = "bad"

####################
# Query Google     #
####################

# The API key and Custom Search Engine are in local environment variables
my_api_key = os.environ['GOOGLE_CSE_API_KEY']
my_cse_id = os.environ['GOOGLE_CSE_ID']

# Defining the search function
# Return value as total results for the given term
def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    response = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
    return int(response['searchInformation']['totalResults'])

# Looping the searches for each option
for option in options:

    # Plain Positive
    plainpositive_results = google_search(positive_attribute)
    print(plainpositive_results) # Just for testing

    # Option + Positive
    positive_results = google_search(f'{option} {positive_attribute}')
    print(positive_results) # Just for testing

    # Option + Negative
    negative_results = google_search(f'{option} {negative_attribute}')
    print(negative_results) # Just for testing

    # Calculate Sentiment Orientiation Score
    SentimentOrientation = math.log(positive_results / plainpositive_results / negative_results / plainpositive_results)

    # Append list with Orientations
    SentimentOrientations.append(SentimentOrientation)

    # Output the Score
    print("Sentiment Score for " + option + " is: " + str(SentimentOrientation))

####################
# Output		   #
####################

# 1) Find highest value for Sentiment orientation, then 2) determine its index, and then 3) call that same item in options list
winner = options[SentimentOrientations.index(max(SentimentOrientations))]

# Let's give some potentially really bad advice
print("We (irresponsibly) recommend going with " + winner + ", which the internet thinks is the best (or least worst).")
