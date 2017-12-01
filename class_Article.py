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

class Article:
    def __init__(self, art_dict={}):
        self.url = art_dict["web_url"]
        self.snippet = art_dict["snippet"]
        self.source = art_dict["source"]
        self.headline = art_dict["headline"]["main"]
        self.keywords = []
        for kw in art_dict["keywords"]:
            self.keywords.append(kw["value"])
        self.published = datetime.strptime(art_dict["pub_date"], "%Y-%m-%dT%H:%M:%S%z")
        self.byline = art_dict["byline"]["original"]

    def LongestWordInAbstract(self):
        return alphabeticOnly(sorted(self.snippet.split(), key=lambda l: len(alphabeticOnly(l)), reverse = True)[0])

    def AgeOfArticle(self):
        return str((datetime.now(timezone.utc) - self.published).days) + " days ago"

    def ToCSVInfo(self):
        return "{},{},{}\n".format(
            alphabeticOnly(self.headline),
            alphabeticOnly(self.byline),
            "|".join(self.keywords))

    def __str__(self):
        return "'{}'\n\t{} (published {})\n\t(Keywords: {})".format(self.headline, self.byline, self.AgeOfArticle(), ','.join(self.keywords))

    def GetArticles(query, count=10):
        nyt_articleSearch_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
        params = {}
        params["api-key"]=NYT_APIKEY
        params["sort"]="newest"
        params["fq"]='source:("The New York Times")' # NYT is the only source that reliably includes keywords
        params["q"]='+'.join(query.split())
        response = Cache.Check(nyt_articleSearch_url, params)
        article_list = []
        for article_dict in response["response"]["docs"]:
            article_list.append(Article(article_dict))
        count = max(min(count, 10), 1) # clamp count between 1 and 10
        # return a list of articles, sorted by the number of keywords
        return sorted(article_list, key=lambda k: len(k.keywords), reverse = True)[:count]
