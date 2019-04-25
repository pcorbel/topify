#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

import cpuinfo
import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on CPU based on:
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)
- The cpuinfo library (https://github.com/workhorsy/py-cpuinfo)

Both of these libs are Docker-compatible,
i.e. they can access host metrics within a Docker container
"""


@dataclass
class CoreStats:
    name: str = ""
    temperature_current: float = 0.0
    temperature_high: float = 0.0
    temperature_critical: float = 0.0

    def collect(self, core) -> None:
        self.name = core.label
        self.temperature_current = core.current
        self.temperature_high = core.high
        self.temperature_critical = core.critical


@dataclass
class CPUCollector(BaseCollector):
    _id: str = "cpu"
    brand: str = ""
    percent: float = 0.0
    percent_per_cpu: List[float] = field(default_factory=list)
    temperature_per_core: List[CoreStats] = field(default_factory=list)
    vendor_id: str = ""

    def collect(self) -> None:
        self.brand = cpuinfo.get_cpu_info().get("brand")
        self.vendor_id = cpuinfo.get_cpu_info().get("vendor_id")
        self.percent = psutil.cpu_percent(percpu=False)
        self.percent_per_cpu = psutil.cpu_percent(percpu=True)

        self.temperature_per_core.clear()
        for core in psutil.sensors_temperatures().get("coretemp", []):
            core_stats = CoreStats()
            core_stats.collect(core)
            self.temperature_per_core.append(core_stats)
