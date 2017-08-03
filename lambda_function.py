from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, convert_errors

from db.datastore import DataStore
from core.kicks import Kicks

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launched():
    return question('Welcome to Daily Kicks')

@ask.intent('HelloIntent')
def hello(firstname):
    print('First name is ', firstname)
    print(convert_errors)
    if 'firstname' in convert_errors or firstname == None:
        # since age failed to convert, it keeps its string
        # value (e.g. "?") for later interrogation.
        return question("Can you please repeat your name?")

    speech_text = render_template('hello', firstname=firstname)
    return statement(speech_text).simple_card('Hello', speech_text)

if __name__ == '__main__':
    app.run()

# import random
# def lambda_handler(event, context):
#     print(event)
#     #upperLimitDict = event['request']['intent']['slots']['firstname']
#     # upperLimit = None
#     # if 'value' in upperLimitDict:
#     #     upperLimit = parseInt(upperLimitDict['value'])
#     # else:
#     #     upperLimit = 100
#
#     number = random.randint(0, 100)
#     response = {
#         'version': '1.0',
#         'response': {
#             'outputSpeech': {
#                 'type': 'PlainText',
#                 'text': 'Your lucky number is ' + str(number),
#             }
#         }
#     }
#
#     return response
