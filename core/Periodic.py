#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Periodic.py
MIT License (c) Marie Faure <dev at faure dot systems>

Base class for periodic actions.
"""

import asyncio
from contextlib import suppress


class Periodic:

    # __________________________________________________________________
    def __init__(self, func, time, logger=None):
        self._logger = logger
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None
        # log creation

    # __________________________________________________________________
    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())
        # log start

    # __________________________________________________________________
    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
        # log stop

    # __________________________________________________________________
    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            self.func()
