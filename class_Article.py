import json
import requests

from project_caching import Cache

NYT_APIKEY = '7fa52abd77be435b8fdd4b0fb37a8ed5'

class Article:
    def __init__(self, art_dict={}):
        self.url = art_dict["web_url"]
        self.snippet = art_dict["snippet"]
        self.source = art_dict["source"]
        self.headline = art_dict["headline"]["main"]
        self.keywords = []
        for kw in art_dict["keywords"]:
            self.keywords.append(kw["value"])
        self.published = art_dict["pub_date"]
        self.byline = art_dict["byline"]["original"]

    def LongestWordInAbstract(self):
        return Article.alphabeticOnly(sorted(self.snippet.split(), key=lambda l: len(Article.alphabeticOnly(l)), reverse = True)[0])

    def ToCSVInfo(self):
        return "{},{},{}\n".format(
            Article.alphabeticOnly(self.headline),
            Article.alphabeticOnly(self.byline),
            "|".join(self.keywords))

    def __str__(self):
        return "'{}'\n\t{} (published {})\n\t(Keywords: {})".format(self.headline, self.byline, self.published, ','.join(self.keywords))

    def alphabeticOnly(word):
        cleanWord = ""
        for s in word:
            if s.isalpha():
                cleanWord += s
        return cleanWord

    def GetArticles(query, API_cache):
        nyt_articleSearch_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
        params = {}
        params["api-key"]=NYT_APIKEY
        params["sort"]="newest"
        params["fq"]='source:("The New York Times")' # NYT is the only source that reliably includes keywords
        params["q"]='+'.join(query.split())
        response = API_cache.Check(nyt_articleSearch_url, params)
        input()
        article_list = []
        for article_dict in response["response"]["docs"]:
            article_list.append(Article(article_dict))
        # return a list of the top 5 articles, sorted by the number of keywords
        return sorted(article_list, key=lambda k: len(k.keywords), reverse = True)[:5]
