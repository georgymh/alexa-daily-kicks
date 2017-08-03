import datetime

from utils.utils import readHTML
from utils.utils import getSessionAndCookies
from utils.utils import getTodaysDate
from utils.utils import NotImplementedException
from utils.utils import ReachedMaxPageNumberException

class PageScraper(object):
    def __init__(self, maxPageNumber = 20, pageNumber = 1):
        self.maxPageNumber = maxPageNumber
        self.currentPage = pageNumber
        self.kicksURLS = []
        self.kicksList = []
        self.currentKicksInPage = 0
        self.totalKicksNumberInPage = 0
        self.session, self.cookies = getSessionAndCookies(self.siteUrl)
        self.loadPage(self.currentPage)

    def getDailyKicks(self):
        """
        Returns kicks for today and tomorrow.
        """
        todaysDate = getTodaysDate()
        for kicks in self.getNextKicks():
            releaseDate = datetime.datetime.strptime(kicks.releaseDate, '%Y-%m-%d')
            diff = releaseDate - todaysDate
            if diff.days > 1:
                break
            yield kicks

    def getNextKicks(self):
        while True:
            while self.currentKicksInPage == self.totalKicksNumberInPage:
                print('###', self.currentKicksInPage, self.totalKicksNumberInPage)
                self.loadNextPage()
            newKicks = self.scrapeKicks(self.kicksURLS[self.currentKicksInPage])
            self.kicksList.append(newKicks)
            self.currentKicksInPage += 1
            yield newKicks

    def loadNextPage(self):
        # Should prevent going to an invalid page.
        self.currentPage += 1
        if self.currentPage > self.maxPageNumber:
            print("Reached max page.")
            print("Printing next page for debugging purposes before exiting...")
            self.loadPage(self.currentPage, debug=True)
            raise ReachedMaxPageNumberException()
        print('Going to next page', self.currentPage)
        self.loadPage(self.currentPage)

    def getAllKicks(self):
        if self.totalKicksNumberInPage == 0:
            self.kicksList = [self.scrapeKicks(kicksURL) for kicksURL in kicksURLS]
            self.kicksList = [kicks for kicks in self.kicksList if kicks is not None]
            self.currentKicksInPage = self.totalKicksNumberInPage
        return self.kicksList

    def loadPage(self, pageNumber, debug = False):
        if pageNumber <= 1:
            html = readHTML(self.siteUrl, self.session, self.cookies)
        else:
            html = readHTML(self.pagedSiteUrl + str(pageNumber), self.session, self.cookies, self.siteUrl)
        if debug:
            print(html)
        self.kicksURLS = self.findKicksURLS(html)
        self.kicksList = []
        self.currentKicksInPage = 0
        self.totalKicksNumberInPage = len(self.kicksURLS)

    def findKicksURLS(self, html):
        raise NotImplementedException()

    def scrapeKicks(self, url):
        raise NotImplementedException()
