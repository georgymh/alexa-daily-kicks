from utils.utils import generateNewCustomId

class Kicks(object):
    def __init__(self, title, style, color, price, releaseDate, description, imageUrls, url, site):
        self.title = title
        if style != 'N/A':
            self.style = style
        else:
            self.style = "DK_" + generateNewCustomId()
        self.color = color
        self.price = price
        self.releaseDate = releaseDate
        self.description = description
        self.imageUrls = imageUrls
        self.url = url
        self.site = site

    def getInfo(self, utf8 = False):
        infoObject = {
            'Title': self.title,
            'Style': self.style,
            'Color': self.color,
            'Price': self.price,
            'ReleaseDate': self.releaseDate,
            'Description': self.description,
            'ImageUrls': [url for url in self.imageUrls],
            'Url': set(self.url),
            'Site': self.site
        }
        if utf8:
            return self.getInfoAsUTF8(infoObject)
        return infoObject

    def _getInfoAsUTF8(self, infoObject):
        for key, val in infoObject.items():
            if type(val) is not list:
                infoObject[key] = val.encode('utf-8')
            else:
                # Could be recursive
                for i, e in enumerate(val):
                    infoObject[key][i] = e.encode('utf-8')
        return infoObject
