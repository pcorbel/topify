#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from dataclasses import dataclass, field
from typing import List

import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on network based on:
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)
- The urllib library  (https://docs.python.org/3/library/urllib.html)

Both of these libs are not Docker-compatible by default,
i.e. they cannot access host metrics within a Docker container.
We have to set network_mode: host to access host metrics
"""


@dataclass
class NicCounters:
    name: str = ""
    bytes_sent: int = 0
    bytes_recv: int = 0
    packets_sent: int = 0
    packets_recv: int = 0
    errin: int = 0
    errout: int = 0
    dropin: int = 0
    dropout: int = 0

    def collect(self, nic, counters) -> None:
        self.name = nic
        self.bytes_sent = counters.bytes_sent
        self.bytes_recv = counters.bytes_recv
        self.packets_sent = counters.packets_sent
        self.packets_recv = counters.packets_recv
        self.errin = counters.errin
        self.errout = counters.errout
        self.dropin = counters.dropin
        self.dropout = counters.dropout


@dataclass
class NetworkIOStats:
    total: NicCounters = NicCounters()
    per_nic: List[NicCounters] = field(default_factory=list)

    def collect(self) -> None:
        self.total.collect("total", psutil.net_io_counters(pernic=False))
        self.per_nic.clear()
        for nic, counters in psutil.net_io_counters(pernic=True).items():
            nic_counters = NicCounters()
            nic_counters.collect(nic, counters)
            self.per_nic.append(nic_counters)


@dataclass
class NetworkCollector(BaseCollector):
    _id: str = "network"
    public_ip: str = ""
    net_io_stats: NetworkIOStats = NetworkIOStats()

    def collect(self) -> None:
        try:
            self.public_ip = (
                urllib.request.urlopen("https://ident.me").read().decode("utf-8")
            )
        except urllib.error.URLError:
            pass
        self.net_io_stats.collect()
