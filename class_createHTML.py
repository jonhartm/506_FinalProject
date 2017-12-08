class CreateHTML:
    def __init__(self, filename, doctitle):
        self.filename = filename
        self.title = doctitle
        self.body = []

    def AddHeading(self, size, sectiontitle):
        self.body.append([size, sectiontitle])

    def AddImage(self, src):
        self.body.append(["img", src])

    def CreateFile(self):
        f = open(self.filename, 'w')
        f.write("<!DOCTYPE html>")
        f.write("<html>")
        f.write("<head>")
        f.write("<title>" + self.title + "</title>")
        f.write("</head>")

        for l in self.body:
            if l[0] == "img":
                f.write("<img src={}>".format(l[1]))
            else:
                f.write("<{}>{}</{}>".format(l[0], l[1], l[0]))

        f.write("<body>")
        f.write("</body>")
        f.write("</html>")
