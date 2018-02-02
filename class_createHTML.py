# creates a basic html file
class CreateHTML:
    def __init__(self, filename, doctitle):
        self.filename = filename
        self.title = doctitle
        self.body = []

    def AddBreak(self):
        self.body.append(["hr"])

    def AddHeading(self, size, sectiontitle):
        self.body.append([size, sectiontitle])

    def AddImage(self, src):
        self.body.append(["img", src])

    def AddLink(self, url, text=""):
        if text == "":
            text = url
        self.body.append(["href", url, text])

    def CreateFile(self):
        f = open(self.filename, 'w')
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")

        f.write("\t<head>\n")
        f.write("\t\t<title>" + self.title + "</title>\n")
        f.write("\t</head>\n")

        f.write("\t<body>\n")
        for l in self.body:
            if l[0] == "img":
                f.write("\t\t<img src={}>\n".format(l[1]))
            elif l[0] == "hr":
                f.write("\t\t<hr>\n")
            elif l[0] == "href":
                f.write("\t\t<a href={}>{}</a>".format(l[1], l[2]))
            else: # all other headings
                f.write("\t\t<{}>{}</{}>\n".format(l[0], l[1], l[0]))
        f.write("\t</body>\n")
        
        f.write("</html>")
