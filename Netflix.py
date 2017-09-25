#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract

# ------------
# netflix_create_cache
# ------------

def create_cache(filename):
    """
    filename is the name of the cache file to load
    returns a dictionary after loading the file or pulling the file from the public_html page
    """
    cache = {}
    filePath = '/u/fares/public_html/netflix-caches/' + filename

    if path.isfile(filename):                   #if file in my local computer
        print('cache found locally')
        with open(filename, "rb") as f:
            cache = pickle.load(f)
    elif path.isfile(filePath):                 #else if file in cs computer
        print('cache found in cs computers')
        with open(filePath, "rb") as f:
            cache = pickle.load(f)
    else:                                       #else retreive from web
        print('cache retreived from web')
        webAddress = 'http://www.cs.utexas.edu/users/fares/netflix-caches/' + \
            filename
        bytes = get(webAddress).content
        cache = pickle.loads(bytes)

    return cache


AVERAGE_RATING = 3.60428996442
YEAR_BY_MOVIE_ID = create_cache(
    'JT26983-MovieYearByMovieID.pickle')
print('success YEAR_BY_MOVIE_ID')
AVERAGE_MOVIE_RATING_BY_RELEASE_YEAR = create_cache(
    'JT26983-AvgMovieRatingsByReleaseYear.pickle')
print('success AVERAGE_MOVIE_RATING_BY_RELEASE_YEAR')
AVERAGE_MOVIE_RATING_BY_MOVIE_ID = create_cache(
    'JT26983-AvgMovieRatingByMovieID.pickle')
print('success AVERAGE_MOVIE_RATING_BY_MOVIE_ID')
AVERAGE_RATING_BY_CUST_ID_AND_REL_YEAR = create_cache(
    'JT26983-AvgRatingByCustomerIDAndReleaseYear.pickle')
print('success AVERAGE_RATING_BY_CUST_ID_AND_REL_YEAR')
ACTUAL_CUSTOMER_RATING = create_cache(
    "JT26983-ActualRatingByCustomerIDAndMovieID.pickle")

# ------------
# netflix_eval
# ------------

def netflix_eval(reader, writer) :
    predictions = []
    actual = []
    # iterate throught the file reader line by line
    for line in reader:
    # need to get rid of the '\n' by the end of the line
        line = line.strip()
        # check if the line ends with a ":", i.e., it's a movie title 
        if line[-1] == ':':
		# It's a movie
            current_movie = line.rstrip(':')
            release_year = YEAR_BY_MOVIE_ID[int(current_movie)]
            avg_movie_rating = AVERAGE_MOVIE_RATING_BY_MOVIE_ID[int(current_movie)]
            avg_rating_release_year = AVERAGE_MOVIE_RATING_BY_RELEASE_YEAR[int(release_year)]
            writer.write(line)
            writer.write('\n')
        else:
		# It's a customer
            current_customer = line
            customer_avg_rating = AVERAGE_RATING_BY_CUST_ID_AND_REL_YEAR[(int(current_customer), int(release_year))]
            prediction = avg_movie_rating + (customer_avg_rating - avg_movie_rating)
            predictions.append(prediction)
            actual.append(ACTUAL_CUSTOMER_RATING[int(current_customer), int(current_movie)])
            writer.write(str(prediction)[:4]) 
            writer.write('\n')	
    # calculate rmse for predications and actuals
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write(str(rmse)[:4] + '\n')

