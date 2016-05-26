#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright 2013, Guy Halford-Thompson
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
########################################################################

import L10n
_ = L10n.get_translation()

import sys
import datetime
from HandHistoryConverter import *

# Ultimate HH Format

class Ultimate(HandHistoryConverter):

    sitename = "Ultimate"
    filetype = "text"
    codepage = ("utf8", "cp1252")
    siteId   = 4
    
    Lim_Blinds = {      '0.20': ('0.05','0.10'),        '0.50': ('0.13', '0.25'),
                        '1.00': ('0.25', '0.50'),          '1': ('0.25', '0.50'),
                        '2.00': ('0.50', '1.00'),          '2': ('0.50', '1.00'),
                        '4.00': ('1.00', '2.00'),          '4': ('1.00', '2.00'),
                        '6.00': ('1.50', '3.00'),          '6': ('1.50', '3.00'),
                        '8.00': ('2.00', '4.00'),          '8': ('2.00', '4.00'),
                       '10.00': ('2.50', '5.00'),         '10': ('2.50', '5.00'),
                       '16.00': ('4.00', '8.00'),         '16': ('4.00', '8.00'),
                       '20.00': ('5.00', '10.00'),        '20': ('5.00', '10.00'),
                       '30.00': ('7.50', '15.00'),        '30': ('7.50', '15.00'),
                       '40.00': ('10.00', '20.00'),       '40': ('10.00', '20.00'),
                       '60.00': ('15.00', '30.00'),       '60': ('15.00', '30.00'),
                       '80.00': ('20.00', '40.00'),       '80': ('20.00', '40.00'),
                      '100.00': ('25.00', '50.00'),      '100': ('25.00', '50.00'),
                      '200.00': ('50.00', '100.00'),     '200': ('50.00', '100.00'),
                      '400.00': ('100.00', '200.00'),    '400': ('100.00', '200.00'),
                      '800.00': ('200.00', '400.00'),    '800': ('200.00', '400.00'),
                      '1000.00': ('250.00', '500.00'),  '1000': ('250.00', '500.00'),
                      '2000.00': ('500.00', '1000.00'), '2000': ('500.00', '1000.00'),
                  }

    # Static regexes
    re_GameInfo     = re.compile("""Hand\s\#(?P<HID>[0-9]+)\,\s(?P<GAME>Hold\'em)
                                    """, re.MULTILINE| re.VERBOSE)
    re_Identify     = re.compile(u'Hand\s\#[0-9]+')
    re_SplitHands   = re.compile('(?:\s?\n){2,}')
    re_TailSplitHands   = re.compile('(\n\n\n+)')
    #re_Button       = re.compile('<ACTION TYPE="HAND_DEAL" PLAYER="(?P<BUTTON>[^"]+)">\n<CARD LINK="[0-9b]+"></CARD>\n<CARD LINK="[0-9b]+"></CARD></ACTION>\n<ACTION TYPE="ACTION_', re.MULTILINE)
    re_PlayerInfo   = re.compile('^(?P<PNAME>.+(posts|is\sdealt|calls|raises|folds|checks))', re.MULTILINE)
    re_Card        = re.compile('^((flop|turn|river):\s\[(?P<CARD>.+)\])', re.MULTILINE)
    #re_BoardLast    = re.compile('^<CARD LINK="(?P<CARD>[0-9]+)"></CARD></ACTION>', re.MULTILINE)
    

    # we need to recompile the player regexs.
    #player_re = '(?P<PNAME>[^"]+)'
    #logging.debug("player_re: " + player_re)
    #<ACTION TYPE="HAND_BLINDS" PLAYER="prato" KIND="HAND_SB" VALUE="0.25"></ACTION>

    re_PostSB           = re.compile(r'^(?P<PNAME>.+)\sposts\ssmall\sblind\s\((?P<SB>[0-9\.]+)\)', re.MULTILINE)
    re_PostBB           = re.compile(r'^(?P<PNAME>.+)\sposts\ssmall\sblind\s\((?P<BB>[0-9\.]+)\)', re.MULTILINE)
   # re_Antes            = re.compile(r'^<ACTION TYPE="HAND_ANTE" PLAYER="%s" VALUE="(?P<ANTE>[.0-9]+)"></ACTION>' % player_re, re.MULTILINE)
   # re_BringIn          = re.compile(r"^%s: brings[- ]in( low|) for \$?(?P<BRINGIN>[.0-9]+)" % player_re, re.MULTILINE)
    #re_FlopPot          = re.compile(r'^<ACTION TYPE="HAND_BOARD" VALUE="BOARD_FLOP" POT="(?P<POT>[.0-9]+)"', re.MULTILINE)
    #re_DrawPot          = re.compile(r'^<ACTION TYPE="HAND_BOARD" POT="(?P<POT>[.0-9]+)"', re.MULTILINE)
    #re_ShowDownPot      = re.compile(r'^<SHOWDOWN NAME="HAND_SHOWDOWN" POT="(?P<POT>[.0-9]+)"', re.MULTILINE)
    #re_PostBoth         = re.compile(r'^<ACTION TYPE="HAND_BLINDS" PLAYER="%s" KIND="HAND_AB" VALUE="(?P<SBBB>[.0-9]+)"></ACTION>' %  player_re, re.MULTILINE)
    
    re_HeroCards        = re.compile(r'^(?P<PNAME>.+)\sis\sdealt\sdown\s\[(?P<CARD>.+)\]', re.MULTILINE)

    #'^<ACTION TYPE="(?P<ATYPE>[_A-Z]+)" PLAYER="%s"( VALUE="(?P<BET>[.0-9]+)")?></ACTION>'
    re_Action           = re.compile(r'^(?P<PNAME>.+)\s(?P<ATYPE>checks|bets|calls|folds|raises)(\sto)?(?P<BET>.*)', re.MULTILINE)

    #re_ShowdownAction   = re.compile(r'<RESULT (WINTYPE="WINTYPE_(HILO|LO|HI)" )?PLAYER="%s" WIN="[.\d]+" HAND="(?P<HAND>\(\$STR_G_FOLD\)|[\$\(\)_ A-Z]+)".+?>(?P<CARDS>(\s+<CARD LINK="[0-9]+"></CARD>){2,5})</RESULT>' %  player_re, re.MULTILINE)
    #<RESULT PLAYER="wig0r" WIN="4.10" HAND="$(STR_G_WIN_TWOPAIR) $(STR_G_CARDS_TENS) $(STR_G_ANDTEXT) $(STR_G_CARDS_EIGHTS)">
    #
    re_CollectPot       = re.compile(r'^(?P<PNAME>.+)\swins\s\((?P<POT>.+)\)', re.MULTILINE)

    def compilePlayerRegexs(self,  hand):
        pass

    def readSupportedGames(self):
        return [["ring", "hold", "nl"]]

    def determineGameType(self, handText):
        info = {}
        m = self.re_GameInfo.search(handText)
        if not m:
            tmp = handText[0:200]
            log.error(_("BossToFpdb.determineGameType: '%s'") % tmp)
            raise FpdbParseError

        mg = m.groupdict()
        #print "DEBUG: mg: %s" % mg
        games = {              # base, category
                  "Hold\'em" : ('hold','holdem'), 
                }
        
        info['type'] = 'ring'
        info['limitType'] = 'nl'
        info['currency'] = 'USD'
        info['sb'] = 0
        info['bb'] = 0

        if 'GAME' in mg:
            (info['base'], info['category']) = games[mg['GAME']]
        # NB: SB, BB must be interpreted as blinds or bets depending on limit type.
        return info


    def readHandInfo(self, hand):
        info = {}
        m = self.re_GameInfo.search(hand.handText)

        if m is None:
            tmp = hand.handText[0:200]
            log.error(_("BossToFpdb.readHandInfo: '%s'") % tmp)
            raise FpdbParseError

        info.update(m.groupdict())
        for key in info:
            if key == 'HID':
                hand.handid = info[key]

    def readButton(self, hand):
        pass

    def readPlayerStacks(self, hand):
        m = self.re_PlayerInfo.finditer(hand.handText)
        players = []
        for a in m:
            hand.addPlayer(0, a.group('PNAME'), 0)

    def markStreets(self, hand):
        # PREFLOP = ** Dealing down cards **
        # This re fails if,  say, river is missing; then we don't get the ** that starts the river.
        if hand.gametype['base'] in ("hold"):
            m =  re.search('<ACTION TYPE="HAND_BLINDS" PLAYER=".+" KIND="(HAND_BB|HAND_SB)" VALUE="[.0-9]+"></ACTION>(?P<PREFLOP>.+(?=<ACTION TYPE="HAND_BOARD" VALUE="BOARD_FLOP")|.+)'
                       '((?P<FLOP><ACTION TYPE="HAND_BOARD" VALUE="BOARD_FLOP" POT="[.0-9]+".+?>.+(?=<ACTION TYPE="HAND_BOARD" VALUE="BOARD_TURN")|.+))?'
                       '((?P<TURN><ACTION TYPE="HAND_BOARD" VALUE="BOARD_TURN" POT="[.0-9]+".+?>.+(?=<ACTION TYPE="HAND_BOARD" VALUE="BOARD_RIVER")|.+))?'
                       '((?P<RIVER><ACTION TYPE="HAND_BOARD" VALUE="BOARD_RIVER" POT="[.0-9]+".+?>.+(?=<SHOWDOWN NAME="HAND_SHOWDOWN")|.+))?', hand.handText,re.DOTALL)
        if hand.gametype['category'] in ('27_1draw', 'fivedraw'):
            m =  re.search(r'(?P<PREDEAL>.+?(?=<ACTION TYPE="HAND_DEAL")|.+)'
                           r'(<ACTION TYPE="HAND_DEAL"(?P<DEAL>.+(?=<ACTION TYPE="HAND_BOARD")|.+))?'
                           r'(<ACTION TYPE="(?P<DRAWONE>.+))?', hand.handText,re.DOTALL)
        #import pprint
        #pprint.pprint(m.groupdict())
        hand.addStreets(m)

    def readCommunityCards(self, hand, street): # street has been matched by markStreets, so exists in this hand
        if street in ('FLOP','TURN','RIVER'):   # a list of streets which get dealt community cards (i.e. all but PREFLOP)
            #print "DEBUG readCommunityCards:", street, hand.streets.group(street)

            boardCards = []
            if street == 'FLOP':
                m = self.re_Card.findall(hand.streets[street])
                for card in m:
                    boardCards.append(self.convertBossCards(card))
            else:
                m = self.re_BoardLast.search(hand.streets[street])
                boardCards.append(self.convertBossCards(m.group('CARD')))

            hand.setCommunityCards(street, boardCards)

    def readAntes(self, hand):
        pass
    
    def readBringIn(self, hand):
        pass
        
    def readBlinds(self, hand):
        liveBlind = True
        for a in self.re_PostSB.finditer(hand.handText):
            if liveBlind:
                hand.addBlind(a.group('PNAME'), 'small blind', a.group('SB'))
                liveBlind = False
            else:
                # Post dead blinds as ante
                hand.addBlind(a.group('PNAME'), 'secondsb', a.group('SB'))
        for a in self.re_PostBB.finditer(hand.handText):
            hand.addBlind(a.group('PNAME'), 'big blind', a.group('BB'))
        for a in self.re_PostBoth.finditer(hand.handText):
            hand.addBlind(a.group('PNAME'), 'both', a.group('SBBB'))

    def readHeroCards(self, hand):
#    streets PREFLOP, PREDRAW, and THIRD are special cases beacause
#    we need to grab hero's cards
        for street in ('PREFLOP', 'DEAL'):
            if street in hand.streets.keys():
                m = self.re_HeroCards.finditer(hand.streets[street])
                newcards = []
                for found in m:
                    hand.hero = found.group('PNAME')
                    for card in self.re_Card.finditer(found.group('CARDS')):
                        newcards.append(self.convertBossCards(card.group('CARD')))
                    hand.addHoleCards(street, hand.hero, closed=newcards, shown=False, mucked=False, dealt=True)

    def convertBossCards(self, card):
        card = int(card)
        retCard = ''
        cardconvert = { 1:'A',
                       10:'T',
                       11:'J',
                       12:'Q',
                       13:'K'}
        realNumber = card % 13 + 1
        if(realNumber in cardconvert):
            retCard += cardconvert[realNumber]
        else:
            retCard += str(realNumber)
       
        if(card > 38):
            retCard += 's'
        elif(card > 25):
            retCard += 'h'
        elif(card > 12):
            retCard += 'c'
        else:
            retCard += 'd'
            
        return(retCard)
    
    def readDrawCards(self, hand, street):
        pass

    def readStudPlayerCards(self, hand, street):
        pass
                    
    def readAction(self, hand, street):
        m = self.re_Action.finditer(hand.streets[street])
        for action in m:
            if action.group('ATYPE') == 'ACTION_FOLD':
                hand.addFold( street, action.group('PNAME'))
            elif action.group('ATYPE') == 'ACTION_CHECK':
                hand.addCheck( street, action.group('PNAME'))
            elif action.group('ATYPE') == 'ACTION_CALL':
                bet = action.group('BET') 
                if Decimal(bet.replace(u',', u''))< hand.lastBet[street]:
                    hand.addCall(street, action.group('PNAME'), bet )
                else:
                    hand.addCallTo(street, action.group('PNAME'), bet )
            elif action.group('ATYPE') == 'ACTION_RAISE':
                bet = action.group('BET') 
                hand.addRaiseTo( street, action.group('PNAME'), bet)
            elif action.group('ATYPE') == 'ACTION_BET':
                hand.addBet( street, action.group('PNAME'), action.group('BET') )
            elif action.group('ATYPE') == 'ACTION_DISCARD':
                hand.addDiscard(street, action.group('PNAME'), action.group('NODISCARDED'), action.group('DISCARDED'))
            elif action.group('ATYPE') == 'ACTION_STAND':
                hand.addStandsPat( street, action.group('PNAME'))
            elif action.group('ATYPE') == 'ACTION_ALLIN':
                bet = action.group('BET')
                player = action.group('PNAME')
                hand.checkPlayerExists(action.group('PNAME'), 'addAllIn')
                bet = bet.replace(u',', u'') #some sites have commas
                Ai = Decimal(bet)
                Bp = hand.lastBet[street]
                if Ai <= Bp:
                    hand.addCallTo(street, player, bet)
                elif Bp == 0:
                    hand.addBet(street, player, bet)
                else:
                    hand.addRaiseTo( street, player, bet)
            else:
                print (_("DEBUG:") + _("Unimplemented %s: '%s' '%s'") % ("readAction", action.group('PNAME'), action.group('ATYPE')))
        self.calculateAntes(street, hand)
                
    def calculateAntes(self, street, hand):
        pass

    def readShowdownActions(self, hand):
        pass

    def readCollectPot(self,hand):
        for m in self.re_CollectPot.finditer(hand.handText):
            potcoll = Decimal(m.group('POT'))
            if potcoll > 0:
                 hand.addCollectPot(player=m.group('PNAME'),pot=potcoll)

    def readShownCards(self,hand):
        pass
