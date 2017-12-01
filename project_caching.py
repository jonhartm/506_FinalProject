import json
import requests

class Cache:
    # Requires a file name.
    # Creates a new file if a file with that name doesn't already exist
    # If that file does exist, loads the dictionary therein to self.cache
    def __init__(self, file_name):
        self.file = file_name
        self.cache = {}
        try:
            with open(file_name, 'r') as f:
                self.cache = json.loads(f.read())
        except Exception as e:
            f = open(file_name, 'w')
            f.close()

    # Checks the cache file for a combination of url and keys to see if it exists in the cache already.
    def Check(self, url, params):
        # create the unique ID to use in the cache
        param_keys = sorted(params.keys()) # sort the paramaters so we know they'll be in the same order even if they aren't in order in the dictionary attribute
        unique_ID = url # start creating the unique_ID with the URL
        for k in param_keys:
            if not("api" in param and "key" in param): # skip anything with the words "api" and "key"
                unique_ID += "_" + k + "_" + params[k].lower()

        # check to see if this unique ID is stored in the cache, and if not, make a request and add it
        if unique_ID in self.cache:
            print("Repeated request - retrieving from cache file.")
            return self.cache[unique_ID]
        else:
            print("New request - adding to cache file.")
            if "flickr" in url: #Flickr is weird, strip off the encapulating parenthesis thing
                response = requests.get(url, params).text[14:-1]
            else:
                response = requests.get(url, params).text
            self.cache[unique_ID] = json.loads(response)
            with open(self.file, 'w') as f:
                f.write(json.dumps(self.cache)) # write the contents of the cache dictionary to the cache file
            return json.loads(response)
