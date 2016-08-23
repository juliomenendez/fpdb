#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .PokerStarsToFpdb import PokerStars


# The idea is the notations we are getting from redline to be
# as close to the pokerstars' one as possible
class Redline(PokerStars):

    sitename = 'Redline'

    substitutions = {
        'LEGAL_ISO': "USD|EUR|GBP|CAD|FPP",
        'LS': u"\$|\xe2\x82\xac|\u20ac|\£|",
        'PLYR': r'\s?(?P<PNAME>.+?)',
        'CUR': u"(\$|\xe2\x82\xac|\u20ac||\£|)",
        'BRKTS': r'(\(button\) |\(small blind\) |\(big blind\) |\(button\) \(small blind\) |\(button\) \(big blind\) )?',
    }

    # As of now the whole hand notation is the same, except for
    # the gameInfo. Redline's stars with: "STD-[SiteName]"
    re_GameInfo = re.compile(u"""
          (STD-\w+)(?P<TITLE>\sGame|\sHand|\sHome\sGame|\sHome\sGame\sHand|Game|\sZoom\sHand|\sGAME)\s\#(?P<HID>[0-9]+):\s+
          (\{.*\}\s+)?(Tournament\s\#                # open paren of tournament info
          (?P<TOURNO>\d+),\s
          # here's how I plan to use LS
          (?P<BUYIN>(?P<BIAMT>[%(LS)s\d\.]+)?\+?(?P<BIRAKE>[%(LS)s\d\.]+)?\+?(?P<BOUNTY>[%(LS)s\d\.]+)?\s?(?P<TOUR_ISO>%(LEGAL_ISO)s)?|Freeroll)\s+)?
          # close paren of tournament info
          (?P<MIXED>HORSE|8\-Game|8\-GAME|HOSE|Mixed\sOmaha\sH/L|Mixed\sHold\'em|Mixed\sPLH/PLO|Mixed\sNLH/PLO|Triple\sStud)?\s?\(?
          (?P<GAME>Hold\'em|HOLD\'EM|Razz|RAZZ|7\sCard\sStud|7\sCARD\sSTUD|7\sCard\sStud\sHi/Lo|7\sCARD\sSTUD\sHI/LO|Omaha|OMAHA|Omaha\sHi/Lo|OMAHA\sHI/LO|Badugi|Triple\sDraw\s2\-7\sLowball|Single\sDraw\s2\-7\sLowball|5\sCard\sDraw|5\sCard\sOmaha(\sHi/Lo)?|Courchevel(\sHi/Lo)?)\)?,?\s
          (?P<LIMIT>No\sLimit|NO\sLIMIT|Limit|LIMIT|Pot\sLimit|POT\sLIMIT|Pot\sLimit\sPre\-Flop,\sNo\sLimit\sPost\-Flop)\s
          (-\s)?
          (?P<SHOOTOUT>Match.*,\s)?
          (Level\s(?P<LEVEL>[IVXLC]+)\s)?
          \(?                            # open paren of the stakes
          (?P<CURRENCY>%(LS)s|)?
          (?P<SB>[.0-9]+)/(%(LS)s)?
          (?P<BB>[.0-9]+)
          (?P<CAP>\s-\s[%(LS)s]?(?P<CAPAMT>[.0-9]+)\sCap\s-\s)?        # Optional Cap part
          \s?(?P<ISO>%(LEGAL_ISO)s)?
          \)                        # close paren of the stakes
          (?P<BLAH2>\s\[AAMS\sID:\s[A-Z0-9]+\])?         # AAMS ID: in .it HH's
          \s-\s
          (?P<DATETIME>.*$)
        """ % substitutions, re.MULTILINE | re.VERBOSE)
