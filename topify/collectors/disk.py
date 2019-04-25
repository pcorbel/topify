#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on disk based on:
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)

This lib is Docker-compatible,
i.e. it can access host metrics within a Docker container
"""


@dataclass
class DiskCollector(BaseCollector):
    _id: str = "disk"
    read_bytes: int = 0
    read_count: int = 0
    write_bytes: int = 0
    write_count: int = 0

    def collect(self) -> None:
        counters = psutil.disk_io_counters()
        self.read_bytes = counters.read_bytes
        self.read_count = counters.read_count
        self.write_bytes = counters.write_bytes
        self.write_count = counters.write_count
