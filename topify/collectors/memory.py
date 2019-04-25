#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on memory based on:
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)

This lib is Docker-compatible,
i.e. it can access host metrics within a Docker container
"""


@dataclass
class RamStats:
    free: float = 0.0
    percent: float = 0.0
    total: float = 0.0
    used: float = 0.0

    def collect(self) -> None:
        ram = psutil.virtual_memory()
        self.free = ram.free
        self.percent = ram.percent
        self.total = ram.total
        self.used = ram.used


@dataclass
class SwapStats:
    free: float = 0.0
    percent: float = 0.0
    total: float = 0.0
    used: float = 0.0

    def collect(self) -> None:
        swap = psutil.swap_memory()
        self.free = swap.free
        self.percent = swap.percent
        self.total = swap.total
        self.used = swap.used


@dataclass
class MemoryCollector(BaseCollector):
    _id: str = "memory"
    ram: RamStats = RamStats()
    swap: SwapStats = SwapStats()

    def collect(self) -> None:
        self.ram.collect()
        self.swap.collect()
