import json

import project_caching as Cache

NYT_APIKEY = '7fa52abd77be435b8fdd4b0fb37a8ed5'

from datetime import datetime, timezone

def alphabeticOnly(word):
    cleanWord = ""
    for s in word:
        if s.isalpha():
            cleanWord += s
    return cleanWord

# returns an Article object based on the dictionary returned from the NYT's article search API
class Article:
    def __init__(self, art_dict={}):
        self.url = art_dict["web_url"]
        self.snippet = art_dict["snippet"]
        self.source = art_dict["source"]
        self.headline = art_dict["headline"]["main"]
        self.keywords = []
        for kw in art_dict["keywords"]:
            self.keywords.append(kw["value"])
        # There are different formats for the published datetime
        if (art_dict["pub_date"])[-1] == "Z":
            self.published = datetime.strptime(art_dict["pub_date"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        else:
            self.published = datetime.strptime(art_dict["pub_date"], "%Y-%m-%dT%H:%M:%S%z")
        self.byline = ""
        if "byline" in art_dict:
            self.byline = art_dict["byline"]["original"]

    # returns the longest word by length in the snippet for this article
    def LongestWordInAbstract(self):
        return alphabeticOnly(sorted(self.snippet.split(), key=lambda l: len(alphabeticOnly(l)), reverse = True)[0])

    # returns a string representing how long ago this article was published.
    # less than 30 days old, "days ago"
    # more than 30 days but less than a year, "months ago"
    # more than a year, "years ago"
    def AgeOfArticle(self):
        days = (datetime.now(timezone.utc) - self.published).days
        if days <= 31:
            return str(days) + " days ago"
        elif days <= 365:
            return str(days//31) + " months ago"
        else:
            return str(days//365) + " years ago"

    # returns a string of the title, user, and list of tags in a CSV writable format
    def ToCSVInfo(self):
        return "{},{},{}\n".format(
            alphabeticOnly(self.headline),
            alphabeticOnly(self.byline),
            "|".join(self.keywords))

    def __str__(self):
        return "'{}'\n\t{} (published {})\n\t(Keywords: {})".format(self.headline, self.byline, self.AgeOfArticle(), ','.join(self.keywords))

    # Checks the NYT api for articles that match the provided query, sorted by the number of keywords provided.
    # Can retrieve between 1 and 100 articles. Default is 10.
    def GetArticles(query, count=10):
        nyt_articleSearch_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
        params = {}
        params["api-key"]=NYT_APIKEY
        params["sort"]="newest"
        params["fq"]='source:("The New York Times")' # NYT is the only source that reliably includes keywords
        params["q"]='+'.join(query.split()) # replace spaces with "+" per API instructions
        params["fl"]="web_url,snippet,source,headline,keywords,pub_date,byline" # filter the response to just the information we want
        article_list = []
        while count > 0:
            params["page"]=str(count-count%10)[0]
            count -= 10
            response = Cache.Check(nyt_articleSearch_url, params)
            for article_dict in response["response"]["docs"]:
                article_list.append(Article(article_dict))

        # return a list of articles, sorted by the number of keywords
        return sorted(article_list, key=lambda k: len(k.keywords), reverse = True)[:count]
