import datetime

from bs4 import BeautifulSoup

from utils.utils import readHTML
from utils.config import SITES
from core.page_scraper import PageScraper
from core.kicks import Kicks
from utils.config import KOF_MAX_PAGE_TO_VISIT_BEFORE_EXITING

class KicksOnFireScraper(PageScraper):
    IDENTIFIER = 'KICKS_ON_FIRE'

    def __init__(self, maxPageNumber = KOF_MAX_PAGE_TO_VISIT_BEFORE_EXITING, pageNumber = 1):
        self.siteUrl = SITES[self.IDENTIFIER]
        self.pagedSiteUrl = self.siteUrl + '?page='
        super().__init__(maxPageNumber, pageNumber)

    def findKicksURLS(self, html):
        soup = BeautifulSoup(html, "html.parser")
        kicksObjects = soup.findAll('div', {'class':"release-date-image-wrapper"})
        urls = [obj.find('a').get('href') for obj in kicksObjects]
        print('urls', urls)
        return urls

    def scrapeKicks(self, url):
        print("GETTING KICK:", url)
        html = readHTML(url, self.session, self.cookies, self.siteUrl)
        soup = BeautifulSoup(html, "html.parser")

        title = soup.findAll('h2', {'class':"head-title"})[0].getText()
        productDetailsSubTag = soup.findAll('div', {'class':"product-details"})[0]\
                                   .findAll('div', {'class':'row'})[0]
        leftColumn = productDetailsSubTag.findAll('div')[0]
        rightColumn = productDetailsSubTag.findAll('div')[1]

        try:
            color = leftColumn.findAll('p')[3].getText()
        except Exception as e:
            print("Error scrapping color:", e)
            color = "N/A"

        try:
            releaseDate = leftColumn.findAll('p')[5].getText()
            releaseDate = datetime.datetime.strptime(releaseDate, '%b. %d, %Y')
            releaseDate = releaseDate.strftime("%Y-%m-%d")
        except Exception as e:
            print("Error scrapping releaseDate:", e)
            releaseDate = "N/A"

        try:
            style = rightColumn.findAll('p', recursive=False)[1].getText()
        except Exception as e:
            print("Error scrapping style:", e)
            style = "N/A"

        try:
            price = productDetailsSubTag.findAll('meta', {'itemprop':'price'})[0]['content']
        except Exception as e:
            print("Error scrapping price:", e)
            price = "N/A"

        try:
            description = soup.findAll('p', {'class':'release-description'})[0].getText()
            description = description.strip()
        except Exception as e:
            print("Error scrapping description:", e)
            description = "N/A"

        try:
            images = soup.findAll('img', {'class':"gallery-img"})
            imageUrls = [i.get('src') for i in images]
        except Exception as e:
            print("Error scrapping imageUrl:", e)
            imageUrls = "N/A"

        kicks = Kicks(title, style, color, price, releaseDate, description, imageUrls, url, self.IDENTIFIER)
        return kicks
