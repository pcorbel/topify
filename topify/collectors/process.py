#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

import psutil

from ..common.base_collector import BaseCollector


"""
Collect all information on processes based on:
- The psutil library  (https://psutil.readthedocs.io/en/latest/#)

The psutil library is not Docker-compatible by default,
i.e. it cannot access host metrics within a Docker container.
We have to set pid: host to access host metrics
"""


@dataclass
class ProcessStats:
    cmdline: List[str] = field(default_factory=list)
    cpu_percent: float = 0.0
    cpu_times: List[float] = field(default_factory=list)
    memory_vms: float = 0.0
    memory_rss: float = 0.0
    memory_percent: float = 0.0
    name: str = ""
    nice: int = 0
    pid: int = 0
    status: str = ""
    username: str = ""

    def collect(self, process) -> None:
        self.cmdline = process.info.get("cmdline")
        self.cpu_percent = process.info.get("cpu_percent")
        self.cpu_times = process.info.get("cpu_times")
        self.memory_vms = process.info.get("memory_info").vms
        self.memory_rss = process.info.get("memory_info").rss
        self.memory_percent = process.info.get("memory_percent")
        self.name = process.info.get("name")
        self.nice = process.info.get("nice")
        self.pid = process.info.get("pid")
        self.status = process.info.get("status")
        self.username = process.info.get("username")


@dataclass
class ProcessCollector(BaseCollector):
    _id: str = "process"
    processes: List[ProcessStats] = field(default_factory=list)

    def collect(self) -> None:
        self.processes.clear()
        for process in psutil.process_iter(
            attrs=[
                "cmdline",
                "cpu_percent",
                "cpu_times",
                "memory_info",
                "memory_percent",
                "name",
                "nice",
                "pid",
                "status",
                "username",
            ]
        ):
            process_stats = ProcessStats()
            process_stats.collect(process)
            self.processes.append(process_stats)
