import json

# FLICKR_KEY = '51525629d45aa9843fcde47a915f6c22'

# removes any non-ascii chars from a string
def AsciiOnly(s):
    return s.encode("ascii", "replace").decode("ascii")

# creates a Photo object based on the dictionary information returned by flickr's flickr.photos.search api ({REQ} REST API #2)
class Photo:
    def __init__(self, photo_dict={}): # {REQ} Constructor 2
        self.id = photo_dict["id"]
        self.owner = photo_dict["owner"] # {REQ} Additional Instance Variables
        self.secret = photo_dict["secret"]
        self.server = photo_dict["server"]
        self.farm = photo_dict["farm"]
        self.title = AsciiOnly(photo_dict["title"])
        self.tags = []
        for t in photo_dict["tags"].split():
            self.tags.append(AsciiOnly(t))

    # returns the source URL for this particular photo
    def SourceUrl(self): # {REQ} Additional Method 2
        return "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(self.farm, self.server, self.id, self.secret)

    def __str__(self): # {REQ} String Method 2
        return self.title + ": (tags: " + ", ".join(self.tags) + ")"
