#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

import docker

from ..common.base_collector import BaseCollector


"""
Collect all information on docker based on:
- The Docker library (https://docker-py.readthedocs.io/en/latest/#)

This lib is not Docker-compatible by default,
i.e. it cannot access host metrics within a Docker container.
We have to mount /var/run/docker.sock to access host metrics
"""


@dataclass
class ServerStats:
    license: str = ""
    os: str = ""
    runtime: str = ""
    version: str = ""

    def collect(self) -> None:
        client = docker.from_env()
        info = client.info()
        self.license = info.get("ProductLicense")
        self.os = info.get("OperatingSystem")
        self.runtime = info.get("DefaultRuntime")
        self.version = info.get("ServerVersion")
        client.close()


@dataclass
class ContainerStats:
    cmd: str = ""
    created: int = 0
    image: str = ""
    name: str = ""
    short_id: str = ""
    state: str = ""
    status: str = ""

    def collect(self, container) -> None:
        self.cmd = container.attrs.get("Command")
        self.created = container.attrs.get("Created")
        self.image = container.attrs.get("Image")
        self.name = container.attrs.get("Names")[0].lstrip("/")
        self.short_id = container.attrs.get("Id")[:12]
        self.state = container.attrs.get("State")
        self.status = container.attrs.get("Status")


@dataclass
class DockerCollector(BaseCollector):
    _id = "docker"
    server: ServerStats = ServerStats()
    containers: List[ContainerStats] = field(default_factory=list)

    def collect(self) -> None:
        client = docker.from_env()
        self.server.collect()
        self.containers.clear()
        for container in client.containers.list(all=True, sparse=True):
            container_stats = ContainerStats()
            container_stats.collect(container)
            self.containers.append(container_stats)
        client.close()
