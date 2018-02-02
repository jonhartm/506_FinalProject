import json
from datetime import datetime, timezone

# returns an Article object based on the dictionary returned from the NYT's article search API ({REQ} REST API #1)
class Article:
    def __init__(self, art_dict={}): # {REQ} Constructor 1
        self.url = art_dict["web_url"]
        self.snippet = art_dict["snippet"]  # {REQ} 3 instance variables 1
        self.source = art_dict["source"]
        self.headline = art_dict["headline"]["main"]
        self.keywords = []
        for kw in art_dict["keywords"]:
            self.keywords.append(kw["value"].split('(')[0].strip()) # strip anything in parens after the keyword - it screws with the Flickr search
        # There are different formats for the published datetime
        # referenced http://strftime.org/ and https://docs.python.org/2/library/datetime.html for datetime parsing
        if (art_dict["pub_date"])[-1] == "Z":
            self.published = datetime.strptime(art_dict["pub_date"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        else:
            self.published = datetime.strptime(art_dict["pub_date"], "%Y-%m-%dT%H:%M:%S%z")
        self.byline = ""
        if "byline" in art_dict: # not all articles have a byline.
            self.byline = art_dict["byline"]["original"]

    def DaysOld(self):
        # referenced answer 2 in https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes
        # for solving the offset-naive and offset aware datetime issue
        return (datetime.now(timezone.utc) - self.published).days

    # returns a string representing how long ago this article was published.
    # less than 30 days old, "days ago"
    # more than 30 days but less than a year, "months ago"
    # more than a year, "years ago"
    def AgeOfArticle(self): # {REQ} Additional Method 1
        days = self.DaysOld()
        if days <= 31:
            return str(days) + " days ago"
        elif days <= 365:
            return str(days//31) + " months ago"
        elif days <= 730:
            return "1 year " + str((days-365)//31) + " months ago"
        else:
            return str(days//365) + " years ago"

    def __str__(self): # {REQ} String Method 1
        return "'{}'\n\t{} (published {})\n\t(Keywords: {})\n".format(self.headline, self.byline, self.AgeOfArticle(), ', '.join(self.keywords[:3]))
