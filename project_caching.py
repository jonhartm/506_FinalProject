import json
import requests
import time as t

from datetime import datetime,time

# ------------------------------------------------------------------------------
# Creates a cache file if one does not already exist, and checks the cache files
# for calls to the API that have already been made. Also handles actually getting
# the reponse from the API, and makes sure calls don't go out too fast
# ------------------------------------------------------------------------------

CACHE_FILE = 'SI506finalproject_cache.json'

API_cache = {}
# referenced https://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
global lastrequest # global variable for tracking the last API call
lastrequest = datetime.now()

# Try to open the cache file if you can find it and load the json data into API_cache
try:
    with open(CACHE_FILE, 'r') as f:
        API_cache = json.loads(f.read())
except Exception as e:
    # print(e)
    print("No cache file named {} exists or I can't read it properly. Creating one now...".format(CACHE_FILE))
    f = open(CACHE_FILE, 'w')
    f.close()

# Checks the cache file for a combination of url and keys to see if it exists in the cache already.
def Check(url, params):
    global lastrequest
    # create the unique ID to use in the cache
    param_keys = sorted(params.keys()) # sort the paramaters so we know they'll be in the same order even if they aren't in order in the dictionary attribute
    unique_ID = url # start creating the unique_ID with the URL
    for k in param_keys:
        if not("api" in k and "key" in k): # skip anything with the words "api" and "key"
            unique_ID += "_" + k + "_" + params[k].lower()

    # check to see if this unique ID is stored in the cache, and if not, make a request and add it
    if unique_ID in API_cache:
        print("Repeated request - retrieving from cache file.")
        return API_cache[unique_ID]
    else:
        print("New request - adding to cache file.")

    # if the last call was less than a second ago, wait one second. NYT API doesn't like it.
    if (datetime.now()-lastrequest).seconds < 1:
        t.sleep(1)
    lastrequest = datetime.now() # set the last request to the current time.

    if "flickr" in url: #Flickr is weird, strip off the encapulating parenthesis thing
        response = requests.get(url, params).text[14:-1]
    else:
        response = requests.get(url, params).text
    API_cache[unique_ID] = json.loads(response)

    f = open(CACHE_FILE, 'w')
    f.write(json.dumps(API_cache)) # write the contents of the cache dictionary to the cache
    return json.loads(response)
