import logging

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, convert_errors

from db.datastore import DataStore
from core.kicks import Kicks
from utils.config import DEFAULT_DATE_FOR_SLOT_SLOT

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('DailyKicksAlexa').setLevel(logging.INFO)

@ask.launch
def launched():
    return question('Welcome to Daily Kicks')

@ask.intent('AskKicksIntent')
def getKicks(item, date):
    # Initial logging
    logging.info('AskKicksIntent was triggered...')
    logging.info('Item is {0}'.format(item))
    logging.info('Date is {0}'.format(date))
    logging.info('Convert errors are {0}'.format(str(convert_errors)))

    # Chech/validate errors
    if 'item' in convert_errors or not item:
        logging.info('Couldn\'t recognize item type... Asking user for clarification.')
        return question("What kind of kicks do you want to know about." + \
                        "You can say jordans, adidas, nike, or general kicks.")
    if 'date' in convert_errors or not date:
        date = DEFAULT_DATE_FOR_SLOT_SLOT
        logging.info('Couldn\'t recognize date... using default ({0})'.format(date))

    # Construct the speech text
    speech_text = "Your daily " + item + " for " + date + " are the following."
    #speech_text = render_template('hello', firstname=firstname)

    # Construct and return the statements/cards/querys/etc to Alexa
    return statement(speech_text).simple_card('Your Daily Kicks', speech_text)

if __name__ == '__main__':
    app.run()
