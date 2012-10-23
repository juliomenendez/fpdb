from flask import Flask
from flask import request

import sys
import os
import os.path
import xml.dom.minidom

import time
import datetime


import Hand
import Configuration
from PokerStarsToFpdb import *
import simplejson as json

application = app = Flask(__name__)
log = logging.getLogger("root")
#Configuration.set_logfile("./fpdb-log.txt")
config = Configuration.Config()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    hand_data = request.form['hand_data']

    con = PokerStars(config, hand_data, '-', 0)

    # Create a list to hold the data object
    hands = []

    # Loop through and process hands
    for hand in con.getProcessedHands():
        h = {
                'sitename' : hand.sitename,
                'gametype' : hand.gametype,
                'handText' : hand.handText,
                'handid' : hand.handid,
                'in_path' : hand.in_path,
                'cancelled' : hand.cancelled,
                'tablename' : hand.tablename,
                'hero' : hand.hero,
                'maxseats' : hand.maxseats,
                'counted_seats' : hand.counted_seats,
                'buttonpos' : hand.buttonpos,
                'runItTimes' : hand.runItTimes,
                'uncalledbets' : hand.uncalledbets,
                'tourNo' : hand.tourNo,
                'tourneyId' : hand.tourneyId,
                'tourneyTypeId' : hand.tourneyTypeId,
                'buyin' : hand.buyin,
                'buyinCurrency' : hand.buyinCurrency,
                'buyInChips' : hand.buyInChips,
                'fee' : hand.fee,
                'level' : hand.level,
                'mixed' : hand.mixed,
                'speed' : hand.speed,
                'isSng' : hand.isSng,
                'isRebuy' : hand.isRebuy,
                'rebuyCost' : hand.rebuyCost,
                'isAddOn' : hand.isAddOn,
                'addOnCost' : hand.addOnCost,
                'isKO' : hand.isKO,
                'koBounty' : hand.koBounty,
                'isMatrix' : hand.isMatrix,
                'isShootout' : hand.isShootout,
                'isZoom' : hand.isZoom,
                'added' : hand.added,
                'addedCurrency' : hand.addedCurrency,
                'tourneyComment' : hand.tourneyComment,
                'seating' : hand.seating,
                'players' : hand.players,
                'posted' : hand.posted,
                'tourneysPlayersIds' : hand.tourneysPlayersIds,
                'bets' : hand.bets,
                'lastBet' : hand.lastBet,
                'streets' : hand.streets,
                'actions' : hand.actions,
                'board' : hand.board,
                'holecards' : hand.holecards,
                'discards' : hand.discards,
                'showdownStrings' : hand.showdownStrings,
                'stacks' : hand.stacks,
                'collected' : hand.collected,
                'collectees' : hand.collectees,
                'folded' : dict.fromkeys(hand.folded),
                'dealt' : dict.fromkeys(hand.dealt),
                'shown' : dict.fromkeys(hand.shown),
                'mucked' : dict.fromkeys(hand.mucked),
                'totalpot' : hand.totalpot,
                'totalcollected' : hand.totalcollected,
                'rake' : hand.rake,
                'sym' : hand.sym

            }
        hands.append(h)


    return json.dumps(hands, use_decimal=True)
    #return parsed_data
    #return hand_data

if __name__ == '__main__':
    app.run(host='0.0.0.0')


