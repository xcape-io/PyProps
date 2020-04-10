#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ThreadingProps.py
MIT License (c) Marie Faure <dev at faure dot systems>

Add asyncio periodic tasks handling to Props base class.
"""

from constants import *
from PropsApp import PropsApp

import threading, time

class ThreadingProps(PropsApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self._publishAllTimerThread = threading.Thread()
        self._publishAllTimerThread = threading.Thread(target=self._publishAllDataThread)
        self._publishAllTimerThread.daemon = True

        self._publishChangesTimerThread = threading.Thread()
        self._publishChangesTimerThread = threading.Thread(target=self._publishDataChangesThread)
        self._publishChangesTimerThread.daemon = True

        self._publishAllTimerThread.start()
        self._publishChangesTimerThread.start()

    # __________________________________________________________________
    def _publishAllDataThread(self):
        # run in its own thread
        while True:
            try:
                self.publishAllData()
            except:
                pass
            finally:
                time.sleep(PUBLISHALLDATA_PERIOD)

    # __________________________________________________________________
    def _publishDataChangesThread(self):
        # run in its own thread
        while True:
            try:
                self.publishDataChanges()
            except:
                pass
            finally:
                time.sleep(PUBLISHDATACHANGES_PERIOD)