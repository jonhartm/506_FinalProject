import json
import project_caching as Cache
from class_Article import Article
from class_Photo import Photo
from class_createHTML import CreateHTML

from API_Keys import NYT_APIKEY, FLICKR_KEY

# Checks the NYT api for articles that match the provided query, sorted by the number of keywords provided.
# Can retrieve between 1 and 100 articles. Default is 10.
def GetArticles(query, API_Key, count=10): # {REQ} Function outside of class definitiion 1
    requestedCount = count
    nyt_articleSearch_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {}
    params["api-key"]=API_Key
    params["sort"]="newest"
    params["fq"]='source:("The New York Times")' # NYT is the only source that reliably includes keywords
    params["q"]='+'.join(query.split()) # replace spaces with "+" per API instructions
    params["fl"]="web_url,snippet,source,headline,keywords,pub_date,byline" # filter the response to just the information we want
    article_list = []
    while count > 0:
        params["page"]=str(count-count%10)[0]
        count -= 10 # subtract 10 from count, since each API call gets 10 articles
        response = Cache.Check(nyt_articleSearch_url, params)
        for article_dict in response["response"]["docs"]:
            new_Article = Article(article_dict) # {REQ} Create Instance 1
            # If the atricle has at least one keyword, add it. Otherwise, skip it and add 1 to count
            if len(new_Article.keywords) != 0:
                article_list.append(Article(article_dict))
            else:
                count += 1
    #Print to the console in the event that no articles could be found
    if len(article_list) == 0:
        print("No articles could be found using search phrase '{}'".format(query))
    # return a list of articles, clipped to the number requested
    trunc_Articles = article_list[:requestedCount]
    # sort the articles based on their age
    return sorted(trunc_Articles, key=lambda d: d.DaysOld()) # {REQ} Sort with Key paramater

# gets a list of from flickr based in the provided query string. Count is the number of photos to return.
def GetPhotos(query, API_Key, count=10): # {REQ} Function outside of class definitiion 2
    # turn query into comma seperated list per API directions. Also ignore very common words.
    split_query = []
    for term in query.split():
        if term not in ["and", "&", "the", "of"]:
            split_query.append(term)

    base_url = "https://api.flickr.com/services/rest/"
    params = {}
    params["api_key"] = API_Key
    params["method"]="flickr.photos.search"
    params["format"]="json"
    params["tags"] = ",".join(split_query)
    params["tag_mode"] = "all"
    params["per_page"] = str(count)
    params["extras"] = "tags"
    params["safe_search"] = "1" # People are weird. Don't risk it.
    response = Cache.Check(base_url, params)
    photo_list = []
    for p in response["photos"]["photo"]:
        photo_list.append(Photo(p)) # {REQ} Create Instance 2
    return photo_list

def GetArticleList(search_term):
    art_list = GetArticles(search_term, NYT_APIKEY)
    print() # add a whitespace
    for a in range(0, len(art_list)):
        print("{}-{}".format(str(a), str(art_list[a]))) # Invoke the str method of 1
    return art_list

#------------------------MAIN-------------------------------------
i = input("Enter a search term: ")
articles = GetArticleList(i)
if len(articles) > 0:
    art_selected = articles[int(input("Enter in the number of the article you would like to find photos for: "))]
    h = CreateHTML(i + "_results.html", "SI 506 Final Project Output: Keyword " + i) # Create Instanceam
    h.AddHeading("h2", art_selected.headline)
    h.AddHeading("h4", "{} ({})".format(art_selected.published, art_selected.AgeOfArticle()))
    h.AddLink(art_selected.url, "Link to Article")
    h.AddHeading("p", art_selected.snippet)
    for k in art_selected.keywords[:3]:
        h.AddBreak()
        photo_search = GetPhotos(k, FLICKR_KEY)
        h.AddHeading("h3", "Keyword: {} ({} photos found)".format(k, len(photo_search)))
        for p in photo_search:
            h.AddHeading("p", p) # Invoke the str method of 2
            h.AddImage(p.SourceUrl())
    h.CreateFile() # {REQ} Create a file for output
    print(h.filename + " has been created.")
