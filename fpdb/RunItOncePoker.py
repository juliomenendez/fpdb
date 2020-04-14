#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .PokerStarsToFpdb import PokerStars


# The idea is the notations we are getting from redline to be
# as close to the pokerstars' one as possible
class RunItOncePoker(PokerStars):

    sitename = 'Run It Once Poker'

    def __init__(
        self,
        config,
        in_path='-',
        out_path='-',
        index=0,
        autostart=True,
        starsArchive=False,
        ftpArchive=False,
        sitename="PokerStars"
    ):
        # HH from RunItOnce Poker is very similar to the PokerStars HH format
        # In here we try to make the needed adjustments and delegate to the the
        # standard PokerStars converter that hopefully gets the job done.
        hand_posted = in_path
        hand_posted = hand_posted.replace('Run It Once Poker ', 'PokerStars ')
        hand_posted = hand_posted.replace('Table ID ', 'Table ')
        hand_posted = hand_posted.replace(',', '')
        in_path = hand_posted

        return super(RunItOncePoker, self).__init__(
            config,
            in_path,
            out_path,
            index,
            autostart,
            starsArchive,
            ftpArchive,
            sitename
        )
