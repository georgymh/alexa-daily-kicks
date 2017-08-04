import datetime
import json
import uuid

def xstr(s):
    return '' if s is None else str(s)

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
