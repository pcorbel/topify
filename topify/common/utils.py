#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import importlib
import inspect
import multiprocessing
import os
import pkgutil
import socketserver

import topify.collectors as plugins

from .base_collector import BaseCollector
from .base_resource import BaseResource


"""
A list of useful methods to find and import collectors
"""


def find_collectors() -> list:
    """
    find_collectors iterates over the plugins directory to find collectors
    """
    collectors = list()
    # Import all modules from topify.collectors
    modules = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules(
            plugins.__path__, plugins.__name__ + "."
        )
    }
    # Iterate through module
    for module in modules.values():
        for name in dir(module):
            obj = getattr(module, name)
            # If object is a subclass of BaseCollector, addind it
            if inspect.isclass(obj):
                if issubclass(obj, BaseCollector) and not obj == BaseCollector:
                    collectors.append(obj)
    return collectors


def expose_collectors(api, collector) -> None:
    """
    expose_collectors starts a collector and exposes it via a Flask endpoint
    """
    # Map resources to collectors and start them
    api.app.logger.info(
        f"Found collector {collector.__name__}. Exposing it on /{collector._id}"
    )
    # Setup Flask resource
    resource = type(
        "resource", (BaseResource,), {"_id": collector._id, "collector": collector()}
    )
    api.add_resource(resource, f"/{collector._id}")
    # Start background collect
    resource().start()
