#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field

from ..common.base_collector import BaseCollector


"""
Collect and expose environment variables
"""


@dataclass
class EnvCollector(BaseCollector):
    _id: str = "env"
    env: dict = field(default_factory=dict)

    def collect(self) -> None:
        self.env = dict(os.environ)
