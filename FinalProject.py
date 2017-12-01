import project_caching
from class_Article import Article
from class_Photo import Photo

ARTICLE_OUTPUT_CSV = 'article_info.csv'
PHOTO_OUTPUT_CSV = 'photo_info.csv'

def ProjectOption2():
    print("Create a new CSV Files...")
    f_article = open(ARTICLE_OUTPUT_CSV, 'w')
    f_article.write("Headline,Byline,Keywords\n")
    f_photo = open(PHOTO_OUTPUT_CSV, 'w')
    f_photo.write("Title,User,Tags,TagCount,URL\n")
    # query = input("Search for Articles about... ")
    query = "Guardian"
    ArticleList = Article.GetArticles(query, API_cache)
    for a in ArticleList:
        print("Article:\n"+ str(a))
        f_article.write(a.ToCSVInfo())
        print("Making a Flickr Search for the longest word in the abstract: " + a.LongestWordInAbstract())
        photo_search = sorted(Photo.GetPhotos(a.LongestWordInAbstract(), API_cache, 20), key=lambda p: p.NumberOfTags())
        for p in photo_search:
            try:
                f_photo.write(p.ToCSVInfo())
                print("\t" + str(p))
            except Exception as e:
                print(e)
                print(p.tags)
    f_article.close()
    f_photo.close()
