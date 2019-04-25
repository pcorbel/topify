#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import time
from dataclasses import dataclass

import distro
import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on host based on:
- The standard platform library (https://docs.python.org/3.7/library/platform.html)
- The standard os library (https://docs.python.org/3.7/library/os.html)
- The distro library (https://distro.readthedocs.io/en/latest/#)
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)

The distro library is not Docker-compatible by default,
i.e. it cannot access host metrics within a Docker container.
We have to mount /etc/os-release to access host metrics

The platform library is not Docker-compatible by default,
i.e. it cannot access host metrics within a Docker container.
We have to set network_mode: host to access host metrics
"""


@dataclass
class HostCollector(BaseCollector):
    _id: str = "host"
    architecture: str = ""
    boot_time: int = 0
    cpu: int = 0
    distro_id: str = ""
    distro_name: str = ""
    distro_version: str = ""
    load_avg_1: float = 0.0
    load_avg_5: float = 0.0
    load_avg_15: float = 0.0
    machine: str = ""
    memory: int = 0
    node: str = ""
    processor: str = ""
    up_time: int = 0

    def collect(self) -> None:
        self.architecture = platform.architecture()[0]
        self.boot_time = psutil.boot_time()
        self.cpu = psutil.cpu_count()
        self.distro_id = distro.id()
        self.distro_name = distro.name()
        self.distro_version = distro.version()
        self.machine = platform.machine()
        self.memory = psutil.virtual_memory().total
        self.node = platform.node()
        self.processor = platform.processor()
        self.load_avg_1, self.load_avg_5, self.load_avg_15 = os.getloadavg()
        self.up_time = round(time.time(), 0) - psutil.boot_time()
