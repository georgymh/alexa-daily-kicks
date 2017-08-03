import datetime
import json
import uuid
import requests

def getSessionAndCookies(url):
    session = requests.Session()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en,es;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    res = session.get(url, headers=headers)
    cookies = dict(res.cookies)
    return session, cookies

def readHTML(url, session, cookies, referer = None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en,es;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    if referer:
        headers['Referer'] = referer
    res = session.get(url,
        verify=False,
        cookies=cookies,
        headers=headers
    )
    return res.text

def getTodaysDate(short: bool = False):
    date = datetime.datetime.combine(
        datetime.datetime.utcnow().date(),
        datetime.datetime.min.time()
    )
    if short:
        return date.strftime("%Y-%m-%d")
    return date

def generateNewCustomId():
    return str(uuid.uuid4()).upper()[:8]

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class NotImplementedException(Exception):
    pass

class ReachedMaxPageNumberException(Exception):
    pass
