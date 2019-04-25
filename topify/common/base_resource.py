#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import multiprocessing
import os
import time
from dataclasses import asdict, dataclass
from typing import Any

import flask_restplus as rest
from diskcache import Cache


"""
The base resource.
It handles the interactions with the cache
"""


@dataclass
class BaseResource(rest.Resource):
    api: Any = None
    cache: Any = Cache("/tmp/topify")
    refresh_interval: int = int(os.getenv("REFRESH_INTERVAL", "3000")) / 1000

    def get(self) -> dict:
        return json.loads(self.cache.get(self._id))

    def start(self) -> None:
        p = multiprocessing.Process(target=self.work)
        p.start()

    def work(self) -> None:
        while True:
            self.collector.collect()
            self.cache.set(self._id, json.dumps(asdict(self.collector)))
            time.sleep(self.refresh_interval)
