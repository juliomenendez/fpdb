
from flask import Flask
from flask import request

import sys
import os
import os.path

import time
import datetime


import Configuration
from PokerStarsToFpdb import *
import Hand
import simplejson as json
from hashlib import sha1
import hmac
import simplejson as json
import urllib

from pkrsess import convert_hand
import logging

log = logging.getLogger("pkrs")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
form = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(form)
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

application = app = Flask(__name__)

config = Configuration.Config()

#consumer_secret = '12345a'

log.info('Loading app')

def ret_error(msg):
    log.error(msg)
    return json.dumps({'status' : 0, 'error' : msg})

def check_signature(secret, raw, sig):
    raw = urllib.unquote(raw.encode('utf-8'))
    log.info('Checking signature')
    hm = hmac.new(consumer_secret, raw, sha1)
    res = hm.hexdigest()
    log.debug('Provided signature ' + sig)
    log.debug('Calculated signature ' + res)
    return sig == res


@app.route('/v1/parse', methods=['GET', 'POST'])
def hand_convert():
    log.info('Hand converter requested')

    # Estract site
    if 'site' in request.form:
        site = request.form['site']
    else:
        site = 'pokerstars'

    # Get consumer id and signature
    #if 'consumer_id' in request.form:
    #    consumer_id = request.form['consumer_id']
    #else:
    #    return ret_error('consumer_id not provided')

    #if 'signature' in request.form:
    #    signature = request.form['signature']
    #else:
    #    return ret_error('Signature not provided')

    # Extract hand data from form
    if 'hand_data' in request.form:
        hand_data = request.form['hand_data']
    else:
        return ret_error('hand_data not provided')

    log.debug('Length of data ' + str(len(hand_data)))

    # Check the sigature is valud
    #if check_signature(consumer_secret, hand_data, signature) == False:
    #    return ret_error('Signature check failed')


    return convert_hand(hand_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

