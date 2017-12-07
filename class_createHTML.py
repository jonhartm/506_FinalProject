import dominate
from dominate.tags import *

class CreateHTML:
    def __init__(self, filename, doctitle):
        self.filename = filename
        self.doc = dominate.document(title = doctitle)

    def AddTitleSection(self, sectiontitle):
        self.doc.add(h2(sectiontitle))

    def AddImageSection(self, title, photodict):
        self.doc.add(h4(title))
        for photo in photodict.keys():
            self.doc.add(p(photo))
            self.doc.add(img(src=photodict[photo]))

    def CreateFile(self):
        f = open(self.filename, 'w')
        f.write(str(self.doc))
