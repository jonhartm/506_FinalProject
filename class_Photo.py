import json
import project_caching as Cache

FLICKR_KEY = '51525629d45aa9843fcde47a915f6c22'

# creates a Photo object based on the dictionary information returned by flickr's flickr.photos.search api
class Photo:
    def __init__(self, photo_dict={}):
        self.id = photo_dict["id"]
        self.owner = photo_dict["owner"]
        self.secret = photo_dict["secret"]
        self.server = photo_dict["server"]
        self.farm = photo_dict["farm"]
        self.title = photo_dict["title"]
        self.tags = []
        for t in photo_dict["tags"].split():
            self.tags.append(t.encode("ascii", "replace").decode("ascii"))

    # returns the source URL for this particular photo
    def SourceUrl(self):
        return "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(self.farm, self.server, self.id, self.secret)

    # returns the number of tags provided for this photo
    def NumberOfTags(self):
        return len(self.tags)

    # returns a string of the title, user, and list of tags in a CSV writable format
    def ToCSVInfo(self):
        return "{},{},{},{}\n".format(
            self.title,
            self.owner,
            "|".join(self.tags),
            str(self.NumberOfTags()),
            self.SourceUrl)

    def __str__(self):
        return "{} - {}".format(self.title, ",".join(self.tags))

    # gets a list of from flickr based in the provided query string. Count is the number of photos to return.
    def GetPhotos(query, count=10):
        count = max(min(count, 100), 1) # clamp count between 1 and 100
        base_url = "https://api.flickr.com/services/rest/"
        params = {}
        params["api_key"] = FLICKR_KEY
        params["method"]="flickr.photos.search"
        params["format"]="json"
        params["tags"] = query
        params["tag_mode"] = "all"
        params["per_page"] = str(count)
        params["extras"] = "tags"
        response = Cache.Check(base_url, params)
        photo_list = []
        for p in response["photos"]["photo"]:
            photo_list.append(Photo(p))
        return photo_list
